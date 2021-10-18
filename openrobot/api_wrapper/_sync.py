import requests
import re
import warnings
import io
import typing
from .error import *
from .results import *

try:
    from urllib.parse import quote_plus as quote
except:
    try:
        from urllib.parse import quote
    except:
        quote = lambda s: s
        warnings.warn('urllib.parse.quote_plus and urllib.parse.quote cannot be found. Things might not be parsed well.')

class SyncClient:
    def __init__(self, token: str = 'I-Am-Testing', *, ignore_warning = False):
        if not token:
            raise NoTokenProvided()
        elif token == 'I-Am-Testing' and not ignore_warning:
            warnings.warn('Using I-Am-Testing token will only let you 5 requests/day (UTC based, will reset on 00:00 UTC) for all `/api` methods and will raise an `openrobot.api_wrapper.error.Forbidden` after you have reached your limit.')

        self.token = str(token)

    # Important methods, but should be used un-regularly by the User itself.

    def _get_authorization_headers(self, token: str = None, *, header = True):
        token = str(token or self.token)
        if header is False:
            return f'token={token}'
        else:
            return {'Authorization': token}

    def _request(self, method: str, url: str, **kwargs):
        url = str(url)

        headers = self._get_authorization_headers()
        if kwargs.get('headers') and isinstance(kwargs.get('headers'), dict):
            hdr = kwargs.pop('headers')
            kwargs['headers'].update(headers)
        else:
            kwargs['headers'] = headers

        if not url.startswith('/'):
            url = url[1:]

        raw = kwargs.pop('raw', False)

        if not url.startswith('api/'):
            url = url[4:]

        if not re.match(rf'^http[s]?://[api.openrobot.xyz|lyrics.ayomerdeka.com]/', url) and not kwargs.pop('no_url_regex', False):
            url = ('https://api.openrobot.xyz/api' + url)
        else:
            raise TypeError('URL is not a valid HTTP/HTTPs URL.')

        with requests.Session() as s:
            r = s.request(method, url, **kwargs)

            js = r.json()
            if r.status_code == 403:
                raise Forbidden(js)
            elif r.status_code == 400:
                raise BadRequest(js)
            elif r.status_code == 500:
                raise InternalServerError(js)
            elif 200 <= r.status_code < 300:
                if raw:
                    return r
                else:
                    return js
            else:
                cls = OpenRobotAPIError(js)
                cls.raw = js

                raise cls

        # Methods to query to API:

    def lyrics(self, query: str) -> LyricResult:
        js = self._request('GET', f'/api/lyrics/{quote(query)}')
        return LyricResult(js)

    def celebrity(self, url: str) -> typing.List[CelebrityResult]:
        js = self._request('GET', '/api/celebrity', params={'url': url})
        return [CelebrityResult(data) for data in js]

    def ocr(self, *, url: str = None, fp: io.BytesIO = None) -> OCRResult:
        if not url and not fp:
            raise OpenRobotAPIError('url and fp kwargs cannot be empty.')
        elif url and fp:
            raise OpenRobotAPIError('url and fp cannot be both not enpty.')

        if url:
            js = self._request('POST', '/api/ocr', params={'url': url})
        else:
            js = self._request('POST', '/api/ocr', files={'upload_file': getattr(fp, 'getvalue', lambda: fp)()})

        return OCRResult(js)

    @property
    def translate(self):
        return self.Translate(self)

    class Translate:
        def __init__(self, client):
            self._client = client

        def __call__(self, text: str, to_lang: str, from_lang: typing.Optional[str] = 'auto') -> TranslateResult:
            js = self._client._request('/api/translate', params={
                'text': text,
                'to_lang': to_lang,
                'from_lang': from_lang
            })
            
            return TranslateResult(js)

        def languages(self):
            js = self._client._request('/api/translate/languages')
            return js