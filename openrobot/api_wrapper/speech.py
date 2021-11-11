import typing
import io
import aiohttp
from .results import SpeechToTextResult, TextToSpeechResult, TextToSpeechSupportResult
from .error import OpenRobotAPIError

class Speech:
    """
    The speech client.
    """

    def __init__(self, client, is_async: bool):
        self._client = client

        self._is_async = is_async

    def speech_to_text(self, source: typing.Union[str, io.BytesIO], language_code: str) -> typing.Union[typing.Coroutine[None, None, SpeechToTextResult], SpeechToTextResult]:
        """|maybecoro|
        
        Speech to text.

        This function is a coroutine if the client is an 
        :class:`AsyncClient` object, else it would be a synchronous method.

        Parameters
        ----------
        source: Union[:class:`str`, :class:`io.BytesIO`]
            The source of the speech. This can be either a URL or a 
            :class:`io.BytesIO` object.
        language_code: :class:`str`
            The language code of the speech.
        voice_id: :class:`str`
            The voice id of the speech.
        engine: :class:`str`
            The engine of the speech.

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
        Union[Coroutine[None, None, :class:`SpeechToTextResult`], :class:`SpeechToTextResult`]
            The result of the text to speech.
        """

        if self._is_async:
            async def _text_to_speech() -> TextToSpeechResult:
                if isinstance(source, str):
                    js = await self._client.request('POST', '/api/speech/speech-to-text', params={'url': source})
                elif isinstance(source, io.BytesIO):
                    data = aiohttp.FormData()
                    data.add_field('file', source)

                    js = await self._client.request('POST', '/api/speech/speech-to-text', data=data)
                else:
                    raise OpenRobotAPIError('source must be a URL or BytesIO.')

                return SpeechToTextResult(js)

            return _text_to_speech()
        else:
            if isinstance(source, str):
                js = self._client.request('POST', '/api/speech/speech-to-text', params={'url': source})
            elif isinstance(source, io.BytesIO):
                data = aiohttp.FormData()
                data.add_field('file', source)

                js = self._client.request('POST', '/api/speech/speech-to-text', files={'upload_file': getattr(source, 'getvalue', lambda: source)()})
            else:
                raise OpenRobotAPIError('source must be a URL or BytesIO.')

            return SpeechToTextResult(js)

    def speech_to_text_support(self) -> typing.Union[typing.Coroutine[None, None, typing.Dict[str, typing.Any]], typing.Dict[str, typing.Any]]:
        """|maybecoro|
        
        Returns the supported details for Speech To Text.

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
        Union[Coroutine[None, None, typing.Dict[:class:`str`, :class:`typing.Any`]], typing.Dict[:class:`str`, :class:`typing.Any`]]
            The supported details for Speech To Text.
        """

        if self._is_async:
            async def _speech_to_text_support() -> typing.Dict[str, typing.Any]:
                js = await self._client.request('GET', '/api/speech/speech-to-text/supports')

                return js

            return _speech_to_text_support()
        else:
            js = self._client.request('GET', '/api/speech/speech-to-text/supports')

            return js
        
    def text_to_speech(self, text: str, language_code: str, voice_id: str, *, engine: str = 'standard') -> typing.Union[typing.Coroutine[None, None, TextToSpeechResult], TextToSpeechResult]:
        """|maybecoro|
        
        Text to speech.

        This function is a coroutine if the client is an 
        :class:`AsyncClient` object, else it would be a synchronous method.

        Parameters
        ----------
        text: :class:`str`
            The text to be speeched.
        language_code: :class:`str`
            The language code of the speech.
        voice_id: :class:`str`
            The voice id of the speech.
        engine: :class:`str`
            The engine of the speech.

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
        Union[Coroutine[None, None, :class:`TextToSpeechResult`], :class:`TextToSpeechResult`]
            The result of the text to speech.
        """

        if self._is_async:
            async def _text_to_speech() -> TextToSpeechResult:
                js = await self._client.request('GET', '/api/speech/text-to-speech', params={'text': text, 'language_code': language_code, 'voice_id': voice_id, 'engine': engine})

                return TextToSpeechResult(js)

            return _text_to_speech()
        else:
            js = self._client.request('GET', '/api/speech/text-to-speech', params={'text': text, 'language_code': language_code, 'voice_id': voice_id, 'engine': engine})

            return TextToSpeechResult(js)

    def text_to_speech_support(self) -> typing.Union[typing.Coroutine[None, None, TextToSpeechSupportResult], TextToSpeechSupportResult]:
        """|maybecoro|

        Returns the supported details for Text To Speech.

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
        Union[Coroutine[None, None, :class:`TextToSpeechSupportResult`], :class:`TextToSpeechSupportResult`]
            The supported details for Text To Speech.
        """

        if self._is_async:
            async def _text_to_speech_support() -> TextToSpeechSupportResult:
                js = await self._client.request('GET', '/api/speech/text-to-speech/supports')

                return TextToSpeechSupportResult(js)

            return _text_to_speech_support()
        else:
            js = self._client.request('GET', '/api/speech/text-to-speech/supports')

            return TextToSpeechSupportResult(js)