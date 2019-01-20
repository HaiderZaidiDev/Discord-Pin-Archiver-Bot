import discord # Imports discord library.
import sys # Imports sys library.

client = discord.Client() # Initializes bot as client.

availServers = client.servers

@client.event # On client event.
async def on_ready(): # When the bot goes online, the following code is executed.
  print(str(client.user) + ' is online.')

@client.event # On client event.
async def on_message(message): # The following code is executed with parameter as message.
  if message.author != client.user: # If the message is **not from a bot, the following code is executed.
    if message.content.startswith('+lastpins'): # If the message starts with +lastpin
      x = await client.pins_from(message.channel)
      pinnedNames = [message.author.name for message in x]
      pinnedAvatars = [message.author.avatar_url for message in x]
      pinnedContent = [message.content for message in x]
      pinnedMsgTime = [message.timestamp for message in x]
      
      
      emb = discord.Embed(description = pinnedContent[0], color = 0xcf1c43)
      emb.set_author(name=pinnedNames[0], icon_url=pinnedAvatars[0])
      emb.set_footer(text=pinnedMsgTime)
      await client.send_message(message.channel, embed=emb) # Outputs message.
    
    if message.content.startswith('+pinned'): # If the message starts with +pinned, the following code is executed.
      pinned = list(await client.pins_from(message.channel)) # List of pins as objects.

      for data in pinned: # Accesses list pinned with iterator data.
        if data.content not in savedPins:
          savedPins.append(data.content)# Appends the content of data to list pinnedMessages (converts obj in list to str)
      

      desc='__**Pinned Messages in #{}:**__ \n \n'.format(message.channel.name) # Creates variable desc, assigned with header of pinned messages.
      for pins in savedPins: # Accesses list pinnedMessages with iterator pinned.
        desc+= pins + '\n \n'  # Adds pinned messages to desc.
      
      emb = discord.Embed(description=desc, color = 0xcf1c43) # Embed for all pinned messages in current channel.
      await client.send_message(message.channel, embed=emb) # Outputs all pinned messages in current channel.
     

        
      
      
      
      
        
client.run(sys.argv[1]) # Runs bot with token as system argument. 
client.close()
  
