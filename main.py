import discord
import sys

client = discord.Client()

@client.event 
async def on_ready():
  print('Operational')

@client.event
async def on_message(message):
  if message.author != client.user:
    if message.content.startswith('+lastpin'):
      pinnedMessages = []
      pinned = list(await client.pins_from(message.channel))

      
      for data in pinned:
        pinnedMessages.append(data.content)
      
      lastPin = pinnedMessages[0]
      emb = discord.Embed(description=lastPin, color = 0xcf1c43)
      await client.send_message(message.channel, embed=emb)
    
    if message.content.startswith('+pinned'):
      pinnedMessages = []
      pinned = list(await client.pins_from(message.channel))

      for data in pinned:
        pinnedMessages.append(data.content)
      
      for pins in pinnedMessages:
        emb = discord.Embed(description=pins, color = 0xcf1c43)
        await client.send_message(message.channel, embed=emb)
        
        
      
      
      
      
        
client.run(sys.argv[1])
client.close()
  
