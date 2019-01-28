#--- Imports
import discord # Imports discord library.
import sys # Imports sys library. 

client = discord.Client() # Initializes bot as client.


@client.event 
async def on_ready(): # When the bot goes online, the following code is executed.
  print(str(client.user) + ' is online.') # Prints operaitonal message.


@client.event
async def on_message(message): # The following code is executed on message event, parameter message.
  userRoles = [role.name for role in message.author.roles]
  if message.author != client.user: # If the message is not from a bot, the following code is executed.
    if message.content.startswith('+lastpin'): # If a user enters a message starting with +lastpin, the following code is executed.
      x = await client.pins_from(message.channel) # Returns list of pins as message objects. 
      pinnedNames = [message.author.name for message in x] # list of names for message objects in x.
      pinnedAvatars = [message.author.avatar_url for message in x] # list of avatar urls for message objects in x.
      pinnedContent = [message.content for message in x] # list of message strings for message objects in x.
      
      emb = discord.Embed(description = pinnedContent[0], color = 0xcf1c43) # Intilializes embed with description as index 0 of pinnedContent.
      emb.set_author(name=pinnedNames[0], icon_url=pinnedAvatars[0]) # Sets the embeds avatar and name that matches to the corresponding information in x.
      await client.send_message(message.channel, embed=emb) # Sends message containing embed to channel message was executed in. 
    
    if message.content.startswith('+maintenance') and message.author.id == '357652932377837589':
      emb = discord.Embed(description = 'Pin Archiver is down for maintenance.', color = 0xcf1c43) # Initalizes embed with description pinContent.
      await client.send_message(discord.Object(id='538545784497504276'), embed=emb) # Sends message containing embed to specified channel (presumably a log channel i.e #pins-archive).
    
    if message.content.startswith('+ping'):
      emb = discord.Embed(description = 'Online.', color = 0xcf1c43) # Intilializes embed with description as index 0 of pinnedContent
      await client.send_message(message.channel, embed=emb) # Sends message containing embed to channel message was executed in. 
      
    if message.content.startswith('+del'):
      if str('Administrator') in userRoles or str('Moderator') in userRoles or message.author.id == '357652932377837589':
        async for message in client.logs_from(discord.Object(id='536761750242983937'), limit = 1):
          lastMessage = message
        await client.delete_message(lastMessage)
    
    if message.content.startswith('+help'):
      helpMsg = '''
       __**Information**__:
        
        This bot was made by @Nitr0us#5090, if you have any questions or require support please contact him.
        
       __**Features**__:
        
        **1)** Last Pinned Message:
        Usage: +lastpin 
        Purpose: Displays the last pinned message of the current channel.
        
        **2)** Archive Pinned Messages to #pin-archive:
        Usage: Automatic
        Purpose: To archive all pinned messages to a channel in case of deletion.  
        
        **3)** Ping:
        Usage: +ping
        Purpose: Notifies you if the bot is online.
        
        **4)** Delete:
        Usage: +del
        Permisssion: Administrators & Moderators
        Purpose: To delete the last pinned message in #pin-archive.
      '''
      emb = discord.Embed(description=helpMsg, color = 0xcf1c43)
      await client.send_message(message.channel, embed=emb)
     
@client.event
async def on_message_edit(before, after): # The following code is executed on message edit even (whenever a message is pinned/edited).
  x = await client.pins_from(before.channel) # Returns list of pins as message objects.
  pinnedContent = [message.content for message in x] # list of strings for message objects in x. 

  
  if before.author != client.user and before.content in pinnedContent and before.author.bot == False: # If the message was not sent by a bot, and is the last pinned message in the channel, the following code is executed.
    name = before.author.name # Name as author of message.
    avatar = before.author.avatar_url # Avatar as avatar url of message author.
    pinContent = before.content # pinContent as string of pinned message.
    msgChannel = before.channel # msgChannel as channel name the message was pinned in.
   
    emb = discord.Embed(description = pinContent, color = 0xcf1c43) # Initalizes embed with description pinContent.
    emb.set_author(name=name, icon_url=avatar) # Sets author and avatar url of the author of pinned message.
    
    if attachments != []:
      attachments = before.attachments
      imgContent = attachments[0]['url']
      emb.set_image(url=imgContent)
      
    emb.set_footer(text='Sent in #{}'.format(msgChannel)) # Sets footer as the channel the message was sent and pinned in.
    await client.send_message(discord.Object(id='536761750242983937'), embed=emb) # Sends message containing embed to specified channel (presumably a log channel i.e #pins-archive).

client.run(sys.argv[1]) # Runs bot with token as system argument. 
client.close()
  
