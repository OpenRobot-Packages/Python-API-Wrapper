from openrobot.api_wrapper import AsyncClient

client = AsyncClient(...)

lyrics = await client.lyrics("Never gonna give you up")
