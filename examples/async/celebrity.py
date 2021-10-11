from openrobot.api_wrapper import AsyncClient

client = AsyncClient(...)

celebrities = await client.celebrity(url=...) # List[openrobot.api_wrapper.results.CelebrityResult]

for celebrity in celebrities:
    celebrity # openrobot.api_wrapper.results.CelebrityResult