from openrobot.api_wrapper import AsyncClient

client = AsyncClient(...)

# Perform Text To Speech

# From file
from io import BytesIO

file_bytes = BytesIO(...)

stt = await client.speech.speech_to_text(file_bytes, language_code=...)

# From URL
url = ...

stt = await client.speech.speech_to_text(url, language_code=...)


stt.text # ...
stt.duration # ...


# Get details on Text To Speech such as supported languages, etc.

await client.speech.speech_to_text_support() # {'languages': ['Language Codes']}