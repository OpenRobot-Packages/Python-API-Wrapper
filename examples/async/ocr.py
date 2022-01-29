from openrobot.api_wrapper import AsyncClient

client = AsyncClient(...)

# From URL:
ocr = await client.ocr(source=...)

# From bytes:
from io import BytesIO
ocr = await client.ocr(source=BytesIO(...))

ocr.text # ...
