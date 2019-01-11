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
      pinned = await client.pins_from(message.channel)
      #await client.send_message(message.channel, pinned.content)
      
      for message in pinned[-1]:
        print(message.content)

client.run(sys.argv[1])
client.close()
  
