import typing

class OpenRobotAPIBaseResult:
    """The base result of the API."""
    def __init__(self, js):
        self.raw = js

class LyricResult(OpenRobotAPIBaseResult):
    """The result of the /api/lyrics endpoint."""
    def __init__(self, js):
        super().__init__(js)

        self.title = js['title']
        self.artist = js['artist']
        self.lyrics = js['lyrics']

class CelebrityResult(OpenRobotAPIBaseResult):
    """The result of the /api/celebrity endpoint."""
    def __init__(self, js):
        super().__init__(js)

        self.confidence: int = js['Confidence']
        self.urls: typing.List[str] = js['URLs']
        self.name: str = js['Name']
        self.gender: typing.Optional[str] = js['Gender'] # TODO: Maybe make this an enum e.g Gender.female or Gender.male
        self.face: self.FaceProperty = self.FaceProperty(js['Face'])

    class FaceProperty:
        """The Face object."""
        def __init__(self, js):
            self.bounding_box: self.BoundingBoxProperty = self.BoundingBoxProperty(js['BoundingBox'])
            self.confidence: int = js['Confidence']
            self.landmarks: typing.List[self.LandmarksProperty] = [self.LandmarksProperty(landmark) for landmark in js['Landmarks']]
            self.pose: self.Pose = self.Pose(js['Pose'])
            self.quality: self.Quality = self.Quality(js['Quality'])
            self.emotion: typing.List[self.Emotion] = [self.Emotion(emotion) for emotion in sorted(js['Emotions'], key=lambda d: d['Confidence'])]
            self.smile: self.Smile = self.Smile(js['Smile'])

        class BoundingBoxProperty:
            def __init__(self, js):
                self.width: int = js['Width']
                self.height: int = js['Height']
                self.left: int = js['Left']
                self.top: int = js['Top']

        class LandmarksProperty:
            def __init__(self, js):
                self.type: str = js['type']
                self.coordinate: self.CoordinateLandmarksProperty = self.CoordinateLandmarksProperty(js['X'], js['Y'])

            class CoordinateLandmarksProperty:
                def __init__(self, x, y):
                    self.x: int = x
                    self.y: int = y

        class Pose:
            def __init__(self, js):
                self.roll: int = js['Roll']
                self.yaw: int = js['Yaw']
                self.pitch: int = js['Pitch']

        class Quality:
            def __init__(self, js):
                self.brightness: int = js['Brightess']
                self.sharpnes: int = js['Sharpness']

        class Emotion:
            def __init__(self, js):
                self.type = js['Type']
                self.confidence = js['Confidence']

        class Smile:
            def __init__(self, js):
                self.value = js['Value']
                self.confidence = js['Confidence']

            def is_smiling(self):
                return self.value is True

class OCRResult(OpenRobotAPIBaseResult):
    """The result of /api/ocr endpoint."""
    def __init__(self, js):
        super().__init__(js)

        self.text = js['text']

class TranslateResult(OpenRobotAPIBaseResult):
    """The result of /api/ocr endpoint."""
    def __init__(self, js):
        super().__init__(js)

        self.to = js[0]['to']
        self.text = js[0]['text']
        self.source = js[0]['source']
        self.before = js[0]['before']