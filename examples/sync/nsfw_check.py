from openrobot.api_wrapper import SyncClient

client = SyncClient(...)

nsfw_check = client.nsfw_check("<Insert URL>")
