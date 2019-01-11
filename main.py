import discord
import sys

client = discord.Client()

@client.event
async def on_message(message):
  if message.author != client.user:
    if message.content.startswith('+pinned'):
      await client.send_message(message.channel, pins_from(message.channel))

client.run(sysargv[1])
client.close()
  
