from openrobot.api_wrapper import AsyncClient

client = AsyncClient(...)

nsfw_check = await client.nsfw_check("<Insert URL>")
