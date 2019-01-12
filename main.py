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
      print(message.author.name)
      pinnedMessages = []
      pinned = list(await client.pins_from(message.channel))

      
      for data in pinned:
        pinnedMessages.append(data.content)
      
      lastPin = pinnedMessages[0]
      emb = discord.Embed(description= '__**Last Pinned Message**__: \n \n' + lastPin, color = 0xcf1c43)
      await client.send_message(message.channel, embed=emb)
    
    if message.content.startswith('+pinned'):
      pinnedMessages = []
      pinned = list(await client.pins_from(message.channel))

      for data in pinned:
        pinnedMessages.append(data.content)
      
      desc='__**Pinned Messages:**__ \n \n'
      for pins in pinnedMessages:
        desc+= pins + '\n \n'  
      
      emb = discord.Embed(description=desc, color = 0xcf1c43)
      await client.send_message(message.channel, embed=emb)
        
        
      
      
      
      
        
client.run(sys.argv[1])
client.close()
  
