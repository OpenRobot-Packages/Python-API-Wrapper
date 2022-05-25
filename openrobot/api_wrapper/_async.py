import aiohttp
import asyncio
import re
import warnings
import io
import typing
from .error import *
from .results import *
from .translate import Translate
from .speech import Speech
from .utils import *

try:
    from urllib.parse import quote_plus as quote
except:
    try:
        from urllib.parse import quote
    except:
        quote = lambda s: s
        warnings.warn(
            'urllib.parse.quote_plus and urllib.parse.quote cannot be found. Things might not be parsed well.')


class AsyncClient:
    """Async Client for OpenRobot API.

    Parameters
    ----------
    token: Optional[:class:`str`]
        The token to be used to authorize to the API. Defaults 
        to ``I-Am-Testing``.
    session: Optional[:class:`aiohttp.ClientSession`]
        The session to be used. Defaults to ``None``.
    loop: Optional[:class:`asyncio.AbstractEventLoop`]
        The loop to be used. Defaults to :meth:`asyncio.get_event_loop`.
    ignore_warning: Optional[:class:`bool`]
        Ignores the ``I-Am-Testing`` Warning. Defaults to ``False``.
    handle_ratelimit: Optional[:class:`bool`]
        Handles the ratelimit. If this is ``False``, then it raises
        :exc:`TooManyRequests`. Else, it will sleep for `Retry-After`. 
        Defaults to ``True``.
    tries: Optional[:class:`int`]
        The number of tries to execute a request to the API This is to. 
        handle 429s. This does not affect anything if ``handle_ratelimit``
        is ``False``. If this is ``None``, it will go infinitely, and you
        might get Temp-Banned by Cloudflare. Defaults to ``5``.

    Attributes
    ----------
    token: :class:`str`
        The token used to authorize to the API.
    loop: :class:`asyncio.AbstractEventLoop`
        The loop that is used.
    session: Optional[:class:`aiohttp.ClientSession`]
        The session used. ``None`` if not specified.
    """

    def __init__(self, token: str = 'I-Am-Testing', *, session: aiohttp.ClientSession = None,
                 loop: asyncio.AbstractEventLoop = None, ignore_warning: bool = False, handle_ratelimit: bool = True,
                 tries: int = 5):
        token = token or get_token_from_file()

        if not token:
            raise NoTokenProvided()
        elif token == 'I-Am-Testing' and not ignore_warning:
            warnings.warn(
                'Using I-Am-Testing token will only let you 5 requests/day (UTC based, will reset on 00:00 UTC) for all `/api` methods and will raise an `openrobot.api_wrapper.error.Forbidden` after you have reached your limit.')

        self.token: str = str(token)

        self.loop: asyncio.AbstractEventLoop = loop or asyncio.get_event_loop()

        self.session: typing.Optional[aiohttp.ClientSession] = session if isinstance(session,
                                                                                     aiohttp.ClientSession) else None

        if self.session:
            self.session._loop = self.loop

        self.handle_ratelimit: bool = handle_ratelimit

        self.tries: int = tries

    # Important and internal methods, but should be used un-regularly by the User itself.

    def _get_authorization_headers(self, token: str = None, *, header=True):
        token = str(token or self.token)
        if header is False:
            return f'token={token}'
        else:
            return {'Authorization': token}

    async def _request(self, method: str, url: str, **kwargs) -> typing.Union[dict, aiohttp.ClientResponse]:
        url = str(url)

        headers = self._get_authorization_headers()
        if kwargs.get('headers') and isinstance(kwargs.get('headers'), dict):
            kwargs['headers'].update(headers)
        else:
            kwargs['headers'] = headers

        return_on = kwargs.pop('return_on', [])

        if not url.startswith('/'):
            url = url[1:]

        raw = kwargs.pop('raw', False)

        if not url.startswith('api/'):
            url = url[4:]

        if not re.match(rf'^http[s]?://[api.openrobot.xyz|lyrics.ayomerdeka.com]/', url) and not kwargs.pop(
                'no_url_regex', False):
            url = ('https://api.openrobot.xyz/api' + url)
        else:
            raise TypeError('URL is not a valid HTTP/HTTPs URL.')

        tries = int(self.tries) if self.tries is not None else None

        while tries is None or tries > 0:
            if self.session:
                async with self.session.request(method, url, **kwargs) as resp:
                    js = await json_or_text(resp)

                    if not isinstance(js, dict):
                        raise UnexpectedContentType(resp, js)

                    if resp.status in return_on:
                        if raw:
                            return resp
                        else:
                            return js
                    elif resp.status == 403:
                        raise Forbidden(resp, js)
                    elif resp.status == 400:
                        raise BadRequest(resp, js)
                    elif resp.status == 500:
                        raise InternalServerError(resp, js)
                    elif resp.status == 429:
                        if not self.handle_ratelimit:
                            raise TooManyRequests(resp, js)

                        try:
                            await asyncio.sleep(int(resp.headers['Retry-After']))
                        except KeyError as e:
                            raise KeyError(
                                'Retry-After header is not present.') from e  # this probably won't trigger, but
                            # either way we still need to handle it, right?

                        if tries:
                            tries -= 1
                    elif 200 <= resp.status < 300:
                        if raw:
                            return resp
                        else:
                            return js
                    else:
                        cls = OpenRobotAPIError(js)
                        cls.raw = js
                        cls.response = resp

                        raise cls
            else:
                async with aiohttp.ClientSession(loop=self.loop) as sess:
                    async with sess.request(method, url, **kwargs) as resp:
                        js = await resp.json()
                        if resp.status in return_on:
                            if raw:
                                return resp
                            else:
                                return js
                        elif resp.status == 403:
                            raise Forbidden(resp, js)
                        elif resp.status == 400:
                            raise BadRequest(resp, js)
                        elif resp.status == 500:
                            raise InternalServerError(resp, js)
                        elif resp.status == 429:
                            if not self.handle_ratelimit:
                                raise TooManyRequests(resp, js)

                            try:
                                await asyncio.sleep(resp.headers['Retry-After'])
                            except KeyError as e:
                                raise KeyError('Retry-After header is not present.') from e

                            if tries:
                                tries -= 1
                        elif 200 <= resp.status < 300:
                            if raw:
                                return resp
                            else:
                                return js
                        else:
                            cls = OpenRobotAPIError(js)
                            cls.raw = js
                            cls.response = resp

                            raise cls

        raise TooManyRequests(resp, js)

    # Methods to query to API:

    async def text_generation(self, text: str, *, max_length: typing.Optional[int] = None,
                              num_return: typing.Optional[int] = 1) -> TextGenerationResult:
        """|coro|

        Text Generation/Completion. This uses the /api/text-generation endpoint.

        Parameters
        ----------
        text: :class:`str`
            The text to be completed/generated.
        max_length: Optional[:class:`int`]
            The maximum length of the generated text. Defaults to ``None``.
        num_return: Optional[:class:`int`]
            The number of generated texts to return. Defaults to 1.

        Raises
        ------
        :exc:`Forbidden`
            API Returned a 403 HTTP Status Code.
        :exc:`BadRequest`
            API Returned a 400 HTTP Status Code.
        :exc:`InternalServerError`
            API Returned a 500 HTTP Status Code.

        Returns
        -------
        :class:`TextGenerationResult`
            The text generation result returned by the API.
        """

        js = await self._request('POST', '/api/text-generation',
                                 data={'text': text, 'max_length': max_length, 'num_return': num_return})
        return TextGenerationResult(js)

    async def text_generation_get(self, task_id: str) -> TextGenerationResult:
        """|coro|

        Gets the status of a text generation task. This uses the /api/text-generation/{task_id} endpoint.

        Parameters
        ----------
        task_id: :class:`str`
            The task ID of the text generation task.

        Raises
        ------
        :exc:`Forbidden`
            API Returned a 403 HTTP Status Code.
        :exc:`BadRequest`
            API Returned a 400 HTTP Status Code.
        :exc:`InternalServerError`
            API Returned a 500 HTTP Status Code.

        Returns
        -------
        :class:`TextGenerationResult`
            The text generation result returned by the API.
        """

        js = await self._request('GET', f'/api/text-generation/{quote(task_id)}')
        return TextGenerationResult(js)

    async def sentiment(self, text: str) -> SentimentResult:
        """|coro|

        Performs a Sentiment check on a text.

        Parameters
        ----------
        text: :class:`str`
            The text to be checked.

        Raises
        ------
        :exc:`Forbidden`
            API Returned a 403 HTTP Status Code.
        :exc:`BadRequest`
            API Returned a 400 HTTP Status Code.
        :exc:`InternalServerError`
            API Returned a 500 HTTP Status Code.

        Returns
        -------
        :class:`SentimentResult`
            The sentiment result returned by the API.
        """

        js = await self._request('POST', '/api/sentiment', data={'text': text})
        return SentimentResult(js)

    async def sentiment_get(self, task_id: str) -> SentimentResult:
        """|coro|

        Gets the status of a sentiment task. This uses the /api/sentiment/{task_id} endpoint.

        Parameters
        ----------
        task_id: :class:`str`
            The task ID of the sentiment task.

        Raises
        ------
        :exc:`Forbidden`
            API Returned a 403 HTTP Status Code.
        :exc:`BadRequest`
            API Returned a 400 HTTP Status Code.
        :exc:`InternalServerError`
            API Returned a 500 HTTP Status Code.

        Returns
        -------
        :class:`SentimentResult`
            The sentiment result returned by the API.
        """

        js = await self._request('GET', f'/api/sentiment/{quote(task_id)}')
        return SentimentResult(js)

    async def summarization(self, text: str, *, max_length: typing.Optional[int] = None,
                            min_length: typing.Optional[int] = 1) -> SummarizationResult:
        """|coro|

        Summarizes a text. This uses the /api/summarization endpoint.

        Parameters
        ----------
        text: :class:`str`
            The text to be summarized.
        max_length: Optional[:class:`int`]
            The maximum length of the summary. Defaults to ``None``.
        min_length: Optional[:class:`int`]
            The minimum length of the summary. Defaults to ``None``.

        Raises
        ------
        :exc:`Forbidden`
            API Returned a 403 HTTP Status Code.
        :exc:`BadRequest`
            API Returned a 400 HTTP Status Code.
        :exc:`InternalServerError`
            API Returned a 500 HTTP Status Code.

        Returns
        -------
        :class:`SummarizationResult`
            The summarization result returned by the API.
        """

        js = await self._request('POST', '/api/summarization',
                                 data={'text': text, 'max_length': max_length, 'min_length': min_length})
        return SummarizationResult(js)

    async def summarization_get(self, task_id: str) -> SummarizationResult:
        """|coro|

        Gets the status of a summarization task. This uses the /api/summarization/{task_id} endpoint.

        Parameters
        ----------
        task_id: :class:`str`
            The task ID of the summarization task.

        Raises
        ------
        :exc:`Forbidden`
            API Returned a 403 HTTP Status Code.
        :exc:`BadRequest`
            API Returned a 400 HTTP Status Code.
        :exc:`InternalServerError`
            API Returned a 500 HTTP Status Code.

        Returns
        -------
        :class:`SummarizationResult`
            The summarization result returned by the API.
        """

        js = await self._request('GET', f'/api/summarization/{quote(task_id)}')
        return SummarizationResult(js)

    async def lyrics(self, query: str) -> LyricResult:
        """|coro|
        
        Gets the lyrics from the API.

        Parameters
        ----------
        query: :class:`str`
            Searches for the lyrics from the query.

        Raises
        ------
        :exc:`Forbidden`
            API Returned a 403 HTTP Status Code.
        :exc:`BadRequest`
            API Returned a 400 HTTP Status Code.
        :exc:`InternalServerError`
            API Returned a 500 HTTP Status Code.

        Returns
        -------
        :class:`LyricResult`
            The Lyrics Result returned by the API.
        """

        js = await self._request('GET', f'/api/lyrics/{quote(query)}', return_on=[404, 200])
        return LyricResult(js)

    async def nsfw_check(self, source: typing.Union[bytes, io.BytesIO]) -> NSFWCheckResult:
        """|coro|
        
        Queries an NSFW Check to the API.

        Parameters
        ----------
        source: Union[:class:`bytes`, :class:`io.BytesIO`]
            The image to be checked.

        Raises
        ------
        :exc:`Forbidden`
            API Returned a 403 HTTP Status Code.
        :exc:`BadRequest`
            API Returned a 400 HTTP Status Code.
        :exc:`InternalServerError`
            API Returned a 500 HTTP Status Code.

        Returns
        -------
        :class:`NSFWCheckResult`
            The NSFW Check Result returned by the API.
        """

        if isinstance(source, bytes):
            source = io.BytesIO(source)

        if not isinstance(source, io.BytesIO):
            raise TypeError('source must be a bytes or BytesIO.')

        data = aiohttp.FormData()
        data.add_field('file', source)

        js = await self._request('POST', '/api/nsfw-check', data=data)
        return NSFWCheckResult(js)

    async def description(self, source: typing.Union[bytes, io.BytesIO]) -> DescriptionResult:
        """|coro|

        Gets the description from the API.

        Parameters
        ----------
        source: Union[:class:`bytes`, :class:`io.BytesIO`]
            The image to be checked.

        Raises
        ------
        :exc:`Forbidden`
            API Returned a 403 HTTP Status Code.
        :exc:`BadRequest`
            API Returned a 400 HTTP Status Code.
        :exc:`InternalServerError`
            API Returned a 500 HTTP Status Code.

        Returns
        -------
        :class:`DescriptionResult`
            The description result returned by the API.
        """

        if isinstance(source, bytes):
            source = io.BytesIO(source)

        if not isinstance(source, io.BytesIO):
            raise TypeError('source must be a bytes or BytesIO.')

        data = aiohttp.FormData()
        data.add_field('file', source)

        js = await self._request('POST', '/api/description', data=data)

        return DescriptionResult(js)

    async def celebrity(self, source: typing.Union[bytes, io.BytesIO]) -> typing.List[CelebrityResult]:
        """|coro|
        
        Detects the celebrities in the image.

        Parameters
        ----------
        source: Union[:class:`bytes`, :class:`io.BytesIO`]
            The source of the image.

        Raises
        ------
        :exc:`Forbidden`
            API Returned a 403 HTTP Status Code.
        :exc:`BadRequest`
            API Returned a 400 HTTP Status Code.
        :exc:`InternalServerError`
            API Returned a 500 HTTP Status Code.

        Returns
        -------
        List[:class:`CelebrityResult`]
            The celebrities detected.
        """

        if isinstance(source, bytes):
            source = io.BytesIO(source)

        if not isinstance(source, io.BytesIO):
            raise TypeError('source must be a bytes or BytesIO.')

        data = aiohttp.FormData()
        data.add_field('file', source)

        js = await self._request('POST', '/api/celebrity', data=data)
        return [CelebrityResult(data) for data in js['celebrities']]

    async def ocr(self, source: typing.Union[bytes, io.BytesIO]) -> OCRResult:
        """|coro|
        
        Reads text from an image.

        Parameters
        ----------
        source: Union[:class:`bytes`, :class:`io.BytesIO`]
            The URL/Bytes of the image.

        Raises
        ------
        :exc:`Forbidden`
            API Returned a 403 HTTP Status Code.
        :exc:`BadRequest`
            API Returned a 400 HTTP Status Code.
        :exc:`InternalServerError`
            API Returned a 500 HTTP Status Code.

        Returns
        -------
        :class:`OCRResult`
            The OCR/Text found.
        """

        if isinstance(source, bytes):
            source = io.BytesIO(source)

        if not isinstance(source, io.BytesIO):
            raise TypeError('source must be a bytes or BytesIO.')

        data = aiohttp.FormData()
        data.add_field('file', source)

        js = await self._request('POST', '/api/ocr', data=data)

        return OCRResult(js)

    @property
    def translate(self) -> Translate:
        """:class:`Translate`: The Translate client."""
        return Translate(self, True)

    # @property
    # def speech(self) -> Speech:
    #     """:class:`Speech`: The Speech client."""
    #     return Speech(self, True)
