from openrobot.api_wrapper import AsyncClient

client = AsyncClient(...)

lyrics = await client.lyrics("Never gonna give you up")

lyrics.title # Never gonna give you up
lyrics.artist # ...
lyrics.lyric