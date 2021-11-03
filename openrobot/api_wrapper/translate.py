import typing
from .results import TranslateResult

class Translate:
    """
    The Translate Client.
    """
    
    def __init__(self, client, is_async: bool):
        self._client = client

        self._is_async = is_async

    def __call__(self, text: str, to_lang: str, from_lang: typing.Optional[str] = 'auto') -> typing.Union[typing.Coroutine[None, None, TranslateResult], TranslateResult]:
        """|maybecoro|
        
        Translates a text.

        This function is a coroutine if the client is an 
        :class:`AsyncClient` object, else it would be a synchronous method.

        Parameters
        ----------
        text: :class:`str`
            The text to be translated.
        to_lang: :class:`str`
            The language to be translated to.
        from_lang: Optional[:class:`str`]
            The text's original language. Defaults to
            ``auto``.

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
        Union[Coroutine[:class:`None`, :class:`None`, :class:`TranslateResult`], :class:`TranslateResult`]
            The Translate Result returned by the API, or a Corountine if 
            the client is a :class:`AsyncClient`.
        """

        if self._is_async:
            async def _do_translate() -> TranslateResult:
                js = await self._client._request('/api/translate', params={
                    'text': text,
                    'to_lang': to_lang,
                    'from_lang': from_lang
                })
                
                return TranslateResult(js)

            return _do_translate
        else:
            js = self._client._request('/api/translate', params={
                'text': text,
                'to_lang': to_lang,
                'from_lang': from_lang
            })
            
            return TranslateResult(js)

    def languages(self) -> typing.Union[typing.Coroutine[None, None, typing.Dict[str, str]], typing.Dict[str, str]]:
        """|maybecoro|

        Gets the translate's supported languages, with the
        Language Name and Language Code.

        This function is a coroutine if the client is an 
        :class:`AsyncClient` object, else it would be a synchronous method.

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
        Union[Coroutine[Dict[:class:`None`, :class:`None`, :class:`str`, :class:`str`]], Dict[:class:`str`, :class:`str`]]
            The supported languages that the transate supports
            in the format of ``{'Language Name': 'Language Code'}``.
        """

        if self._is_async:
            async def _languages() -> typing.Dict[str, str]:
                js = await self._client._request('/api/translate/languages')
                return js

            return _languages
        else:
            js = self._client._request('/api/translate/languages')
            return js