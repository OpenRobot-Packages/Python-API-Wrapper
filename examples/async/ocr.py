from openrobot.api_wrapper import AsyncClient

client = AsyncClient(...)

# From URL:
ocr = await client.ocr(url=...)

# From bytes:
from io import BytesIO
ocr = await client.ocr(fp=BytesIO(...))

ocr.text # ...