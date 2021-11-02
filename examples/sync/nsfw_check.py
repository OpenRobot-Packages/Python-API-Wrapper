from openrobot.api_wrapper import AsyncClient

client = SyncClient(...)

nsfw_check = client.nsfw_check("<Insert URL>")

for label in nsfw_check.labels:
    label.name # ...
    label.parent_name # ...
    label.confidence # 0 - 100

nsfw_check.score # 0 - 1