from openrobot.api_wrapper import AsyncClient

client = AsyncClient(...)

celebrities = await client.celebrity(url=...)  # List[openrobot.api_wrapper.results.CelebrityResult]

