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
      
      
      emb = discord.Embed(description = pinnedContent[0], color = 0xcf1c43)
      emb.set_author(name=pinnedNames[0], icon_url=pinnedAvatars[0])
      emb.set_footer(text=pinnedMsgTime)
      await client.send_message(message.channel, embed=emb) # Outputs message.
    

@client.event
async def on_message_edit(before, after):
  if before.author != client.user and message.type == discord.MessageType.pins_add:
    name = before.author.name
    avatar = before.author.avatar_url
    pinContent = before.content
    msgChannel = before.channel
  
    emb = discord.Embed(description = pinContent, color = 0xcf1c43)
    emb.set_author(name=name, icon_url=avatar)
    emb.set_footer(text='Sent in # {}'.format(msgChannel))
    await client.send_message(discord.Object(id='536761750242983937'), embed=emb) # Outputs message.

      
     

      
        
client.run(sys.argv[1]) # Runs bot with token as system argument. 
client.close()
  
