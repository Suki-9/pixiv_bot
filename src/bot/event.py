from bot import client
from bot import tree

@client.event
async def on_ready():
  await tree.sync()
