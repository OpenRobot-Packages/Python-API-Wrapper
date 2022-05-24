import typing


class OpenRobotAPIBaseResult:
    """
    The base result of the API.
    
    Attributes
    ----------
    raw: :class:`dict`
        The raw data given by the API.
    """

    def __init__(self, js):
        self.raw = js


class TextGenerationResult(OpenRobotAPIBaseResult):
    """
    The result of the /api/text-generation endpoint.

    Attributes
    ----------
    task_id: :class:`str`
        The Task ID of the request. This is used to re-get
        the result later.
    text: :class:`str`
        The original text passed.
    max_length: :class:`int`
        The maximum length of the generated text.
    num_return: :class:`str`
        The number of generated texts to return.
    status: Literal["STARTED", "PENDING", "COMPLETED", "FAILED"]
        The status of the request. 
    result: Optional[:class:`str`]
        The generated text. This may be ``None`` if status is not
        ``COMPLETED``.
    timestamp: :class:`float`
        The timestamp at which the request was made.
    """

    def __init__(self, js):
        super().__init__(js)

        self.task_id: str = js["task_id"]
        self.text: str = js["text"]
        self.max_length: int = js["max_length"]
        self.num_return: int = js["num_return"]
        self.status: str = js["status"]
        self.result: typing.Optional[typing.List[str]] = [x["generated_text"] for x in js["result"]] if js[
            "result"] else None
        self.timestamp: float = js["timestamp"]


class SentimentResultReturned:
    """
    The sentiment result.

    Attributes
    ----------
    label: Literal["POSITIVE", "NEGATIVE"]
        The label of the sentiment.
    score: :class:`float`
        The score of the sentiment.
    """

    def __init__(self, js):
        self.label: str = js["label"]
        self.score: float = js["score"]


class SentimentResult(OpenRobotAPIBaseResult):
    """
    The resullt of the /api/sentiment endpoint.

    Attributes
    ----------
    task_id: :class:`str`
        The Task ID of the request. This is used to re-get
        the result later.
    text: :class:`str`
        The original text passed.
    status: Literal["STARTED", "PENDING", "COMPLETED", "FAILED"]
        The status of the request. 
    result: List[:class:`SentimentResultReturned`]
        The sentiment result. This may be an empty list if status is not
        ``COMPLETED``.
    timestamp: :class:`float`
        The timestamp at which the request was made.
    """

    def __init__(self, js):
        super().__init__(js)

        self.task_id: str = js["task_id"]
        self.text: str = js["text"]
        self.status: str = js["status"]
        self.result: typing.List[SentimentResultReturned] = [SentimentResultReturned(x) for x in js["result"]]
        self.timestamp: float = js["timestamp"]


class SummarizationResult(OpenRobotAPIBaseResult):
    """
    The result of the /api/summarization endpoint.

    Attributes
    ----------
    task_id: :class:`str`
        The Task ID of the request. This is used to re-get
        the result later.
    text: :class:`str`
        The original text passed.
    max_length: :class:`int`
        The maximum length of the generated text.
    min_length: :class:`str`
        The number of generated texts to return.
    status: Literal["STARTED", "PENDING", "COMPLETED", "FAILED"]
        The status of the request. 
    result: Optional[:class:`str`]
        The generated text. This may be ``None`` if status is not
        ``COMPLETED``.
    timestamp: :class:`float`
        The timestamp at which the request was made.
    """

    def __init__(self, js):
        super().__init__(js)

        self.task_id: str = js["task_id"]
        self.text: str = js["text"]
        self.max_length: int = js["max_length"]
        self.num_return: int = js["min_length"]
        self.status: str = js["status"]
        self.result: typing.Optional[str] = js["result"][0]["summary_text"] if js["result"] else None
        self.timestamp: float = js["timestamp"]


class LyricImages:
    """
    The Lyric's Track Images.

    Attributes
    ----------
    background: Optional[:class:`str`]
        The background image of the track. ``None`` if not found.
    track: Optional[:class:`str`]
        The track image. ``None`` if not found.
    """

    def __init__(self, js):
        self.background: typing.Optional[str] = js.get('background')
        self.track: typing.Optional[str] = js.get('track')


class LyricResult(OpenRobotAPIBaseResult):
    """
    The result of the /api/lyrics endpoint.
    
    Attributes
    ----------
    title: Optional[:class:`str`]
        The title of the song. ``None`` if not found.
    artist: Optional[:class:`str`]
        The artist of the song. ``None`` if not found.
    lyrics: Optional[:class:`str`]
        The lyrics of the song.  ``None`` if not found.
    images: :class:`LyricImages`
        Represents The Lyric's Track Images.
    """

    def __init__(self, js):
        super().__init__(js)

        self.title: str = js['title']
        self.artist: str = js['artist']
        self.lyrics: str = js['lyrics']

        self.images = LyricImages(js.get('images', {}))


class NSFWCheckAdult:
    """
    Checks if the image is adult content.

    Attributes
    ----------
    is_adult: :class:`bool`
        If the image is part of adult content or not
    adult_score: :class:`float`
        The adult score for the image from 0 to 1.
    """

    def __init__(self, js):
        self.is_adult: bool = js['is_adult']
        self.adult_score: float = js['adult_score']


class NSFWCheckRacy:
    """
    Checks if the image is racy content.

    Attributes
    ----------
    is_racy: :class:`bool`
        If the image is part of racy content or not
    raxy_score: :class:`float`
        The racy score for the image from 0 to 1.
    """

    def __init__(self, js):
        self.is_racy: bool = js['is_racy']
        self.racy_score: float = js['racy_score']


class NSFWCheckGore:
    """
    Checks if the image is gore content.

    Attributes
    ----------
    is_gore: :class:`bool`
        If the image is part of gore content or not
    gore_score: :class:`float`
        The gore score for the image from 0 to 1.
    """

    def __init__(self, js):
        self.is_gore: bool = js['is_gore']
        self.gore_score: float = js['gore_score']


class NSFWCheckResult(OpenRobotAPIBaseResult):
    """
    The result of the /api/nsfw-check endpoint.
    
    Attributes
    ----------
    adult: :class:`NSFWCheckAdult`
        Checks if the image is adult content.
    racy: :class:`NSFWCheckRacy`
        Checks if the image is racy content.
    gore: :class:`NSFWCheckGore`
        Checks if the image is gore content.
    """

    def __init__(self, js):
        super().__init__(js)

        self.image_url = js['image_url']
        self.adult = NSFWCheckAdult(js['adult'])
        self.racy = NSFWCheckRacy(js['racy'])
        self.gore = NSFWCheckGore(js['gore'])


class CelebrityFaceRectangle:
    """
    The Celebrity's Face Rectangle (Bounding Box).

    Attributes
    ----------
    left: Union[:class:`int`, :class:`float`]
        X-coordinate of the top left point of the face, in pixels.
    top: Union[:class:`int`, :class:`float`]
        Y-coordinate of the top left point of the face, in pixels.
    width: Union[:class:`int`, :class:`float`]
        Width measured from the top-left point of the face, in pixels.
    height: Union[:class:`int`, :class:`float`]
        Height measured from the top-left point of the face, in pixels.
    """

    def __init__(self, js):
        self.left: typing.Union[int, float] = js['left']
        self.top: typing.Union[int, float] = js['top']
        self.width: typing.Union[int, float] = js['width']
        self.height: typing.Union[int, float] = js['height']


class CelebrityResult(OpenRobotAPIBaseResult):
    """
    The result of the /api/celebrity endpoint.
    
    Attributes
    ----------
    name: :class:`str`
        The name of the Celebrity.
    confidence: Union[:class:`int`, :class:`float`]
        The confidence of the Celebrity.
    face: :class:`CelebrityFaceProperty`
        The face rectangle of the Celebrity.
    """

    def __init__(self, js):
        super().__init__(js)

        self.name: str = js['name']
        self.confidence: typing.Union[int, float] = js['confidence']
        self.face_rectangle: CelebrityFaceRectangle = CelebrityFaceRectangle(js['face_rectangle'])


class SpeechToTextResult(OpenRobotAPIBaseResult):
    """
    The result of /api/speech/speech-to-text endpoint.

    Attributes
    ----------
    text: :class:`str`
        The text of the recognized speech.
    duration: Union[:class:`int`, :class:`float`]
        The time taken to recognize the text in the speech in
        seconds.
    """

    def __init__(self, js):
        super().__init__(js)

        self.text: str = js['text']
        self.duration: typing.Union[int, float] = js['duration']


class TextToSpeechResult(OpenRobotAPIBaseResult):
    """
    The result of /api/speech/text-to-speech endpoint.

    Attributes
    ----------
    url: :class:`str`
        The URL of the speech
    """

    def __init__(self, js):
        super().__init__(js)

        self.url: str = js['url']


class TextToSpeechSupportLanguage:
    """
    The languages supported by Text To Speech.

    Attributes
    ----------
    code: :class:`str`
        The language code.
    name: :class:`str`
        The human-readable language name.
    """

    def __init__(self, js):
        self.code: str = js.get('code')
        self.name: str = js.get('name')


class TextToSpeechSupportVoice:
    """
    The supported voices for Text To Speech.

    Attributes
    ----------
    gender: :class:`str`
        The voice's gender.
    id: :class:`str`
        The Voice ID.
    language: :class:`TextToSpeechSupportLanguage`
        The language of the voice.
    name: :class:`str`
        The Voice's name.
    """

    def __init__(self, js):
        self.gender: str = js.get('Gender')
        self.id: str = js.get('Id')
        self.language: TextToSpeechSupportLanguage = TextToSpeechSupportLanguage(
            {'code': js.get('LanguageCode'), 'name': js.get('LanguageName')})
        self.name: str = js.get('Name')


class TextToSpeechSupportResult(OpenRobotAPIBaseResult):
    """
    The result of /api/speech/text-to-speech/support endpoint.

    Attributes
    ----------
    languages: List[:class:`str`]
        The languages supported by Text To Speech.
    voices: List[:class:`TextToSpeechSupportVoice`]
        The supported voices for Text To Speech.
    """

    def __init__(self, js):
        super().__init__(js)

        self.languages: typing.List[str] = js['languages']
        self.voices: typing.List[TextToSpeechSupportVoice] = [TextToSpeechSupportVoice(voice) for voice in js['voices']]


class OCRResult(OpenRobotAPIBaseResult):
    """
    The result of /api/ocr endpoint.
    
    Attributes
    ----------
    text: :class:`str`
        The OCR Result.
    """

    def __init__(self, js):
        super().__init__(js)

        self.text: str = js['text']


class TranslateResult(OpenRobotAPIBaseResult):
    """
    The result of /api/ocr endpoint.
    
    Attributes
    ----------
    to: :class:`str`
        The language that it was translated to.
    text: :class:`str`
        The translated text.
    source: :class:`str`
        The language of the original text.
    before: :class:`str`
        The original text.
    """

    def __init__(self, js):
        super().__init__(js)

        self.to: str = js[0]['to']
        self.text: str = js[0]['text']
        self.source: str = js[0]['source']
        self.before: str = js[0]['before']
