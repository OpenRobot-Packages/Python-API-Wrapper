from openrobot.api_wrapper import SyncClient

client = SyncClient(...)

# Perform Text To Speech

# From file
from io import BytesIO

file_bytes = BytesIO(...)

stt = client.speech.speech_to_text(file_bytes, language_code=...)

# From URL
url = ...

stt = client.speech.speech_to_text(url, language_code=...)


stt.text # ...
stt.duration # ...


# Get details on Text To Speech such as supported languages, etc.

client.speech.speech_to_text_support() # {'languages': ['Language Codes']}