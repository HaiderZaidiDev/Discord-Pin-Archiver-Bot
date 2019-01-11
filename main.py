import discord
import sys

client = discord.Client()

@client.event 
async def on_ready():
  print('Operational')

@client.event
async def on_message(message):
  if message.author != client.user:
    if message.content.startswith('+pinned'):
      pinned = list(await client.pins_from(message.channel))
      #await client.send_message(message.channel, pinned.content)
      
      for data in pinned:
        lastPin = data.values[-1]
        await client.send_message(message.channel, lastPin.content)
client.run(sys.argv[1])
client.close()
  
