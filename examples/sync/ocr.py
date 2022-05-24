from io import BytesIO
from openrobot.api_wrapper import SyncClient

client = SyncClient(...)

ocr = client.ocr(BytesIO(...))
