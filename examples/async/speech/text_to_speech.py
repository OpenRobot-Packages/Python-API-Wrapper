from openrobot.api_wrapper import AsyncClient

client = AsyncClient(...)

# Perform Text to speech

text = 'Hello World'

tts = await client.speech.text_to_speech(text, 'en-US', ...) # Get it by doing details (Speech.text_to_speech_support)

tts_url = tts.url # https://cdn.openrobot.xyz/speech/text-to-speech/...

# Get details on Speech To Text such as a list of Voices from a specific language, etc.

tts_support = await client.speech.text_to_speech_support('en-US')

for language in tts_support.languages:
    language.name
    language.code

for voice in tts_support.voices:
    voice.gender
    voice.id
    voice.language.name
    voice.language.code
    voice.name