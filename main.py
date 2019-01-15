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
    if message.content.startswith('+lastpin'): # If the message starts with +lastpin
      pinnedMessages = [] # Creates empty list.
      pinned = list(await client.pins_from(message.channel)) # List of pins as objects. 
      
      messageObj = client.get_message('357659724390334465', '534554680005623828')
      
      for ids in messageObj:
        print(message.author)
   
      for data in pinned: # Accesses list pinned with iterator data.
        pinnedMessages.append(data.content) # Appends the content of data to list pinnedMessages (converts obj in list to str)
      
      lastPin = pinnedMessages[0] # Last pinned message in pinnedMessages (The list of pinned messages is ordered newest - oldest)
      emb = discord.Embed(description= '__**Last Pinned Message**__: \n \n' + lastPin, color = 0xcf1c43) # Embed for last pinned message.
      await client.send_message(message.channel, embed=emb) # Outputs message.
    
    if message.content.startswith('+pinned'): # If the message starts with +pinned, the following code is executed.
      pinnedMessages = [] # Creates empty list. 
      pinned = list(await client.pins_from(message.channel)) # List of pins as objects.

      for data in pinned: # Accesses list pinned with iterator data.
        pinnedMessages.append(data.content)# Appends the content of data to list pinnedMessages (converts obj in list to str)
      
      desc='__**Pinned Messages:**__ \n \n' # Creates variable desc, assigned with header of pinned messages.
      for pins in pinnedMessages: # Accesses list pinnedMessages with iterator pinned.
        desc+= pins + '\n \n'  # Adds pinned messages to desc.
      
      emb = discord.Embed(description=desc, color = 0xcf1c43) # Embed for all pinned messages in current channel.
      await client.send_message(message.channel, embed=emb) # Outputs all pinned messages in current channel.
        
        
      
      
      
      
        
client.run(sys.argv[1]) # Runs bot with token as system argument. 
client.close()
  
