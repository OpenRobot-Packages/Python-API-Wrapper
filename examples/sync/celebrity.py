from openrobot.api_wrapper import SyncClient

client = SyncClient(...)

celebrities = client.celebrity(url=...) # List[openrobot.api_wrapper.results.CelebrityResult]

for celebrity in celebrities:
    celebrity # openrobot.api_wrapper.results.CelebrityResult