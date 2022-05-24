from openrobot.api_wrapper import SyncClient

client = SyncClient(...)

# List supported languages:
client.translate.languages()  # Return a dict in a format of {'Language Name': 'Language Code'}

# Translate:
translate = client.translate(text=..., to_lang=...,
                             from_lang=...)  # from_lang param is Optional, it defaults to "auto".
