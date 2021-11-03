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

class LyricResult(OpenRobotAPIBaseResult):
    """
    The result of the /api/lyrics endpoint.
    
    Attributes
    ----------
    titie: :class:`str`
        The title of the song.
    artist: :class:`str`
        The artist of the song.
    lyrics :class:`str`
        The lyrics of the song. 
    """

    def __init__(self, js):
        super().__init__(js)

        self.title: str = js['title']
        self.artist: str = js['artist']
        self.lyrics: str = js['lyrics']

class NSFWLabel:
    """
    NSFW Label.
    
    Attributes
    ----------
    confidence: Union[:class:`int`, :class:`float`]
        The confidence of this NSFW Label. A float/int with 
        a number from 0 - 1.
    """

    def __init__(self, js):
        self.confidence: typing.Union[int, float] = js['Confidence']
        self.parent_name: str = js['ParentName']
        self.name: str = js['Name']

class NSFWCheckResult(OpenRobotAPIBaseResult):
    """
    The result of the /api/nsfw-check endpoint.
    
    Attributes
    ----------
    labels: :class:`NSFWLabel`
        The labels for the image.
    score: Union[:class:`int`, :class:`float`]
        The NSFW rate. A float/int with a number 
        from 0 - 100.
    """

    def __init__(self, js):
        super().__init__(js)

        self.labels: typing.List[NSFWLabel] = [NSFWLabel(x) for x in js['labels']]
        self.score: typing.Union[int, float] = js['nsfw_score']

class CelebrityFaceBoundingBoxProperty:
    """
    The Celebrity's Face Bounding Box.

    Attributes
    ----------
    width: Union[:class:`int`, :class:`float`]
        The width of the bounding box.
    height: Union[:class:`int`, :class:`float`]
        The height of the bounding box.
    left: Union[:class:`int`, :class:`float`]
        The left of the bounding box.
    top: Union[:class:`int`, :class:`float`]
        The top of the bounding box.
    """

    def __init__(self, js):
        self.width: typing.Union[int, float] = js['Width']
        self.height: typing.Union[int, float] = js['Height']
        self.left: typing.Union[int, float] = js['Left']
        self.top: typing.Union[int, float] = js['Top']

class CelebrityFaceLandmarksCoordinateLandmarksProperty:
    """
    The cooridnate of a landmark.

    Attributes
    ----------
    x: Union[:class:`int`, :class:`float`]
        The ``X`` coordinate of the landmark.
    y: Union[:class:`int`, :class:`float`]
        The ``Y`` coordinate of the landmark.
    """

    def __init__(self, x, y):
        self.x: typing.Union[int, float] = x
        self.y: typing.Union[int, float] = y

class CelebrityFaceLandmarksProperty:
    """
    The face landmarks in the current face.

    Attributes
    ----------
    type: :class:`str`
        The type of the landmark. There can be a 
        lot of variety of types e.g ``eyeRight``, 
        ``eyeLeft``, ``nose``, ``mouthRight``, 
        ``mouthLeft``, etc.
    coordinate: :class:`CelebrityFaceLandmarksCoordinateLandmarksProperty`
        The coordinate of the landmark.
    """

    def __init__(self, js):
        self.type: str = js['type']
        self.coordinate: CelebrityFaceLandmarksCoordinateLandmarksProperty = CelebrityFaceLandmarksCoordinateLandmarksProperty(js['X'], js['Y'])

class CelebrityFacePose:
    """
    The pose of the face, from Roll, Yaw and Pitch.

    Attributes
    ----------
    roll: Union[:class:`int`, :class:`float`]
        The roll of the face.
    yaw: Union[:class:`int`, :class:`float`]
        The yaw of the face.
    pitch: Union[:class:`int`, :class:`float`]
        The pitch of the face.
    """

    def __init__(self, js):
        self.roll: typing.Union[int, float] = js['Roll']
        self.yaw: typing.Union[int, float] = js['Yaw']
        self.pitch: typing.Union[int, float] = js['Pitch']

class CelebrityFaceQuality:
    """
    The quality of the face.

    Attributes
    ----------
    brightness: Union[:class:`int`, :class:`float`]
        The brightness of the face.
    sharpness: Union[:class:`int`, :class:`float`]
        The sharpness of the face.
    """

    def __init__(self, js):
        self.brightness: typing.Union[int, float] = js['Brightess']
        self.sharpnes: typing.Union[int, float] = js['Sharpness']

class CelebrityFaceEmotion:
    """
    The emotion of the face.

    Attributes
    ----------
    type: :class:`str`
        The emotion type/name.
    confidence: Union[:class:`int`, :class:`float`]
        The confidence of the emotion.
    """

    def __init__(self, js):
        self.type: str = js['Type']
        self.confidence: typing.Union[int, float] = js['Confidence']

class CelebrityFaceSmile:
    """
    Represents the smile that the celebrity is having, if any.

    Attributes
    ----------
    value: :class:`bool`
        Represents if the celebrity is smiling or not.
    confidence: Union[:class:`int`, :class:`float`]
        The confidence of the celebrity is smiling.
    """

    def __init__(self, js):
        self.value: bool = js['Value']
        self.confidence: typing.Union[int, float] = js['Confidence']

    def is_smiling(self) -> bool:
        """:class:`bool`: True if the celebrity is smiling, else False."""
        return self.value is True

class CelebrityFaceProperty:
    """
    The Face object.

    Attributes
    ----------
    bounding_box: :class:`CelebrityFaceBoundingBoxProperty`
        The bounding box of the Celebrity's face.
    confidence: Union[:class:`int`, :class:`float`]
        The confidence of the face properties.
    landmarks: List[CelebrityFaceLandmarksProperty]
        The landmarks in the face.
    pose: :class:`CelebrityFacePose`
        The pose of the celebrity.
    quality: :class:`CelebrityFaceQuality`
        The quality of the face
    emotion: List[:class:`CelebrityFaceEmotion`]
        The emotions of the face.
    smile: :class:`CelebrityFaceSmile`
        Represents the smile that the celebrity is having.
    """
    
    def __init__(self, js):
        self.bounding_box: CelebrityFaceBoundingBoxProperty = CelebrityFaceBoundingBoxProperty(js['BoundingBox'])
        self.confidence: typing.Union[int, float] = js['Confidence']
        self.landmarks: typing.List[CelebrityFaceLandmarksProperty] = [CelebrityFaceLandmarksProperty(landmark) for landmark in js['Landmarks']]
        self.pose: CelebrityFacePose = CelebrityFacePose(js['Pose'])
        self.quality: CelebrityFaceQuality = CelebrityFaceQuality(js['Quality'])
        self.emotion: typing.List[CelebrityFaceEmotion] = [CelebrityFaceEmotion(emotion) for emotion in sorted(js['Emotions'], key=lambda d: d['Confidence'])]
        self.smile: CelebrityFaceSmile = CelebrityFaceSmile(js['Smile'])

class CelebrityResult(OpenRobotAPIBaseResult):
    """
    The result of the /api/celebrity endpoint.
    
    Attributes
    ----------
    confidence: Union[:class:`int`, :class:`float`]
        The match confidence for the recognized celebrity.
    urls: List[:class:`str`]
        A list of URLs representing the author.
    name: :class:`str`
        The name of the detected celebrity.
    gender: Optional[:class:`str`]
        The gender of the celebrity.
    face: :class:`CelebrityFaceProperty`
        The face object.
    """
    
    def __init__(self, js):
        super().__init__(js)

        self.confidence: typing.Union[int, float] = js['Confidence']
        self.urls: typing.List[str] = js['URLs']
        self.name: str = js['Name']
        self.gender: typing.Optional[str] = js['Gender'] # TODO: Maybe make this an enum e.g Gender.female or Gender.male
        self.face: CelebrityFaceProperty = CelebrityFaceProperty(js['Face'])

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