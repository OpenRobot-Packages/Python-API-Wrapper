from openrobot.api_wrapper import SyncClient

client = SyncClient(...)

# From URL:
ocr = client.ocr(url=...)

# From bytes:
from io import BytesIO
ocr = client.ocr(fp=BytesIO(...))

ocr.text # ...