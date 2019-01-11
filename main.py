import discord
import sys

client = discord.Client()

@client.event 
async def on_ready():
  print('Operational')

@client.event
async def on_message(message):
  pinnedMessages = []
  if message.author != client.user:
    if message.content.startswith('+pinned'):
      pinned = list(await client.pins_from(message.channel))
      last_pin = pinned[-1]
      #await client.send_message(message.channel, pinned.content)
      
      for data in pinned:
        pinnedMessages.append(data)
      
      print(pinnedMessages)
        
client.run(sys.argv[1])
client.close()
  
