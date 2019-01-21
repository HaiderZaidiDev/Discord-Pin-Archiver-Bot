import discord # Imports discord library.
import sys # Imports sys library.

client = discord.Client() # Initializes bot as client.

availServers = client.servers

@client.event # On client event.
async def on_ready(): # When the bot goes online, the following code is executed.
  print(str(client.user) + ' is online.')

@client.event # On client event.
async def on_message(message): # The following code is executed with parameter as message.
  savedPins = []
  if message.author != client.user: # If the message is **not from a bot, the following code is executed.
    if message.content.startswith('+lastpin'): # If the message starts with +lastpin
      pinnedMessages = [] # Creates empty list.
      authorNames = []
      pinned = list(await client.pins_from(message.channel)) # List of pins as objects. 
   
      for data in pinned: # Accesses list pinned with iterator data.
        pinnedMessages.append(data.content) # Appends the content of data to list pinnedMessages (converts obj in list to str)
      
      lastPin = pinnedMessages[0] # Last pinned message in pinnedMessages (The list of pinned messages is ordered newest - oldest)
      emb = discord.Embed(description= '__**Last Pinned Message in #{}**__: \n \n'.format(message.channel.name) + lastPin, color = 0xcf1c43) # Embed for last pinned message.
      await client.send_message(message.channel, embed=emb) # Outputs message.

@client.event
async def on_message_edit(before):
  print(before)
        
      
      
      
      
        
client.run(sys.argv[1]) # Runs bot with token as system argument. 
client.close()
  
