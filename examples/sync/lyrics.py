from openrobot.api_wrapper import SyncClient

client = SyncClient(...)

lyrics = client.lyrics("Never gonna give you up")

lyrics.title # Never gonna give you up
lyrics.artist # ...
lyrics.lyric