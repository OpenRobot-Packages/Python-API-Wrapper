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

try:
    from urllib.parse import quote_plus as quote
except:
    try:
        from urllib.parse import quote
    except:
        quote = lambda s: s
        warnings.warn('urllib.parse.quote_plus and urllib.parse.quote cannot be found. Things might not be parsed well.')

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

    Attributes
    ----------
    token: :class:`str`
        The token used to authorize to the API.
    loop: :class:`asyncio.AbstractEventLoop`
        The loop that is used.
    session: Optional[:class:`aiohttp.ClientSession`]
        The session used. ``None`` if not specified.
    """

    def __init__(self, token: str = 'I-Am-Testing', *, session: aiohttp.ClientSession = None, loop: asyncio.AbstractEventLoop = None, ignore_warning: bool = False):
        if not token:
            raise NoTokenProvided()
        elif token == 'I-Am-Testing' and not ignore_warning:
            warnings.warn('Using I-Am-Testing token will only let you 5 requests/day (UTC based, will reset on 00:00 UTC) for all `/api` methods and will raise an `openrobot.api_wrapper.error.Forbidden` after you have reached your limit.')

        self.token = str(token)

        self.loop = loop or asyncio.get_event_loop()

        self.session = session if isinstance(session, aiohttp.ClientSession) else None

        if self.session:
            self.session._loop = self.loop

    # Important and internal methods, but should be used un-regularly by the User itself.

    def _get_authorization_headers(self, token: str = None, *, header = True):
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

        return_on = kwargs.get('return_on', [])

        if not url.startswith('/'):
            url = url[1:]

        raw = kwargs.pop('raw', False)

        if not url.startswith('api/'):
            url = url[4:]

        if not re.match(rf'^http[s]?://[api.openrobot.xyz|lyrics.ayomerdeka.com]/', url) and not kwargs.pop('no_url_regex', False):
            url = ('https://api.openrobot.xyz/api' + url)
        else:
            raise TypeError('URL is not a valid HTTP/HTTPs URL.')
        
        if self.session:
            async with self.session.request(method, url, **kwargs) as resp:
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

    # Methods to query to API:

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

    async def nsfw_check(self, url: str) -> NSFWCheckResult:
        """|coro|
        
        Queries an NSFW Check to the API.

        Parameters
        ----------
        url: :class:`str`
            The Image URL to check for.

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

        js = await self._request('GET', '/api/nsfw-check', params={'url': url})
        return NSFWCheckResult(js)

    async def celebrity(self, url: str) -> typing.List[CelebrityResult]:
        """|coro|
        
        Detects the celebrities in the image.

        Parameters
        ----------
        url: :class:`str`
            The Image URL.      

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
        
        js = await self._request('GET', '/api/celebrity', params={'url': url})
        return [CelebrityResult(data) for data in js]

    async def ocr(self, source: typing.Union[str, io.BytesIO]) -> OCRResult:
        """|coro|
        
        Reads text from a image.

        Parameters
        ----------
        source: Union[:class:`str`, :class:`io.BytesIO`]
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

        if isinstance(source, str):
            js = await self._request('POST', '/api/ocr', params={'url': source})
        elif isinstance(source, io.BytesIO):
            data = aiohttp.FormData()
            data.add_field('file', source)

            js = await self._request('POST', '/api/ocr', data=data)
        else:
            raise OpenRobotAPIError('source must be a URL or BytesIO.')

        return OCRResult(js)

    @property
    def translate(self) -> Translate:
        """:class:`Translate`: The Translate client."""
        return Translate(self, True)

    @property
    def speech(self) -> Speech:
        """:class:`Speech`: The Speech client."""
        return Speech(self, True)