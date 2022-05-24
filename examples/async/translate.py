from openrobot.api_wrapper import AsyncClient

client = AsyncClient(...)

# List supported languages:
await client.translate.languages()  # Return a dict in a format of {'Language Name': 'Language Code'}

# Translate:
translate = await client.translate(text=..., to_lang=...,
                                   from_lang=...)  # from_lang param is Optional, it defaults to "auto".
