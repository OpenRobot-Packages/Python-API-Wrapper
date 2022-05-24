from openrobot.api_wrapper import SyncClient

client = SyncClient(...)

celebrities = client.celebrity(url=...)  # List[openrobot.api_wrapper.results.CelebrityResult]
