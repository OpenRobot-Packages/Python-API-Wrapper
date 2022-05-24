from io import BytesIO
from openrobot.api_wrapper import AsyncClient

client = AsyncClient(...)

ocr = await client.ocr(BytesIO(...))
