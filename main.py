import argparse
import configparser
import discord
import sys
import asyncio
import sqlite3
from ast import literal_eval

client = discord.Client()
file_path = '/home/pinarchiver/pinArchiver/db'
db=sqlite3.connect('{}/pinarchiver_config.db'.format(file_path))
cursor = db.cursor()
config = None
TOKEN = None

@client.event
async def on_ready():
    """Print a startup message."""
    print(str(client.user) + ' is online.')
    await client.change_presence(activity=discord.Game(name='v2.0 | +help'))

@client.event
async def on_guild_join(guild):
    """Creates a pin-archive channel if one was not already found."""
    available_channels = [channels.name for channels in guild.channels]
    await asyncio.sleep(1)
    role_names = [roles.name for roles in guild.roles]
    bot_role = None
    for i in range(len(role_names)):
        if role_names[i] == 'Pin Archiver':
            bot_role = guild.roles[i] # Bot role object.
    bot_id = 533383387763965982
    bot = await guild.fetch_member(bot_id)

    try:
        if str('pin-archive') not in available_channels:
            channel = await guild.create_text_channel('pin-archive',
                topic="An archive of all pinned messages")
            await channel.set_permissions(guild.default_role, send_messages=False)
            await channel.set_permissions(bot, send_messages=True)
            emb = discord.Embed(
                description = '''Created channel named "pin-archive" as one was not found.''',
                color=0x7289da)
            await channel.send(embed=emb)

    except discord.errors.Forbidden:
        emb = discord.Embed(
            description='''Error: Pin Archiver does not have permission to manage roles, channels or both. These are required for the bot to function. ''',
            color=0x7289da
        )
        emb.set_footer(text='Need assistance? Join the support server: https://discord.gg/jY9xADW')

        #Attempts to send message in every channel until one permits it.
        for channel in guild.channels:
            try:
                await channel.send(embed=emb)
                break
            except:
                pass

async def error(message, error_message):
    emb = discord.Embed(
        description ='Error: {}'.format(error_message),
        color=0x7289da
        )
    emb.set_footer(text='Need assistance? Join the support server: https://discord.gg/jY9xADW')
    await message.channel.send(embed=emb)

@client.event
async def archive_channel_id(after):
    """Determines archive channel for a guild in which the message was sent in."""
    available_channel_names = [channels.name for channels in after.guild.channels]
    available_channel_ids = [channels.id for channels in after.guild.channels]

    if str('pin-archive') not in available_channel_names:
        await on_guild_join(after.guild)

    for i in range (len(available_channel_names)):
        if available_channel_names[i] == str('pin-archive'):
            ARCHIVE_CHANNEL = available_channel_ids[i]
            return ARCHIVE_CHANNEL # Returns the channel id of the archive channel

async def available_channels(message):
    available_channels = [channels.name for channels in message.guild.channels]
    return available_channels

async def archive_message(message):
    """Forwards a message to the archive channel."""
    try:
        name = message.author.display_name
        avatar = message.author.avatar_url
        pin_content = message.content
        server = message.guild.id

        emb = discord.Embed(
            description=pin_content,
            color=0x7289da)  # Initalizes embed with description pin_content.
        emb.set_author(
            name=name,
            icon_url=avatar,
            url='https://discordapp.com/channels/{0}/{1}/{2}'.format(
                server, message.channel.id, message.id)
            )  # Sets author and avatar url of the author of pinned message.

            # Set attachemnt image url as embed image if it exists
        if message.attachments:
            img_url = message.attachments[0].url
            emb.set_image(url=img_url)

        # Sets footer as the channel the message was sent and pinned in.
        emb.set_footer(text='Sent in #{}'.format(message.channel))

        if str('pin-archive') not in await available_channels(message):
            await on_guild_join(message.guild)
            #if str('pin-archive') not in available_channels:

        if str('pin-archive') in await available_channels(message):
            channel = client.get_channel(await archive_channel_id(message))
            await channel.send(embed=emb)

    except discord.errors.Forbidden:
        await error(message, 'Pin Archiver does not have permission to send messages in #pin-archive.')

async def confirm_message(after):
    """ Returns bool true if the channel the message was pinned in is not readable by all roles. """
    channel_perms = after.channel.overwrites # Returns dictionary of overwrites in the current channel
    roles = after.guild.roles # Returns all roles in the guild
    perm_roles = []
    perm_values = []

    for i in range(len(roles)): # Filters roles which have specific channel permissions
        if roles[i] in channel_perms:
             perm_roles.append(roles[i])

    for j in range(len(perm_roles)):
        role_perms = channel_perms[perm_roles[j]].pair() # Tuple containing the roles permission values
        allow, deny = role_perms
        perm_values.append(deny.value)

    if 1024 in perm_values: # Permission value for READ_MESSAGES
        return True

async def message_read_perms(message):
    """Returns True if any of the reader's roles have the manage_messages permission."""
    user_roles = message.author.roles
    role_perms = []
    for i in range(len(user_roles)):
        perm_value = discord.Permissions(permissions=user_roles[i].permissions.value)

        if perm_value.manage_messages or perm_value.administrator or message.author.id == message.guild.owner_id:
            role_perms.append('True')
    if 'True' in role_perms:
        return True



async def invalid_perms(message):
    emb = discord.Embed(
        description='Error: Sorry, you must have the manage_messages permission to execute this command.',
        color=0x7289da
    )
    await message.channel.send(embed=emb)

@client.event
async def on_message_edit(before, after):
    """Main function for handling message edit events."""
    channelPins = await before.channel.pins()
    pinned_ids = [message.id for message in channelPins]
    attachments = after.attachments

    if before.content == after.content and after.author != client.user and len(pinned_ids) == 50:
        oldest_pin = await after.channel.fetch_message(pinned_ids[-1])
        try:
            await oldest_pin.unpin()
        except discord.errors.Forbidden:
            await error(before, '''This channel has reached the maximum pin limit, Pin Archiver can't unpin the oldest message as it does not have the manage messages permission. This message has been archived but not pinned. ''')

    if after.pinned and after.author != client.user:
        private_channel_status = await confirm_message(after)
        if private_channel_status == True:
            warning_message = '''
                        This message was sent in a private channel, archiving it will allow everyone to view it. Do you still want to archive it?
                     '''
            emb = discord.Embed(
                description=warning_message,
                color=0x7289da,
                title='Confirm Action'
                )

            #emb.set_footer(text='Note: You can disable this message by entering {command}.') #Command not yet created.
            confirm_action = await after.channel.send(embed=emb)
            confirmation_emojis = ['✅', '❌']

            for emoji in confirmation_emojis:
                await confirm_action.add_reaction(emoji)

            reaction, user = await client.wait_for('reaction_add',
                check=lambda reaction, user: (user.id != client.user.id) and (reaction.emoji in confirmation_emojis)
                ) # Checks the user reaction, ensuring the reaction is not from a bot.
            if reaction.emoji == '✅':
                await archive_message(after)
                await asyncio.sleep(2)
                await confirm_action.delete()
            if reaction.emoji == '❌':
                await asyncio.sleep(2)
                await confirm_action.delete()
        else:
            await archive_message(after)

@client.event
async def on_reaction_add(reaction, user):
    """Scans for reactions on messages."""
    if reaction.emoji == '📌':
        guild_react_count = cursor.execute("select react_count from config_settings where guild_id = ?", (reaction.message.guild.id,)).fetchone()[0]
        if reaction.count == guild_react_count:
            await reaction.message.pin()

@client.event
async def on_message(message):
    """Handle commands."""
    # If the message is not from a bot, the following code is executed.
    if message.author != client.user:
        if message.content.startswith('+setreactcount'):
            if not await message_read_perms(message):
                await invalid_perms(message)
                return
            try:
                react_count_config = int(message.content[14:len(message.content)]) #Isolates int from message

            except ValueError:
                await error(message, 'The react count must be an integer greater than 0.')
                return

            if react_count_config < 1 or react_count_config > 1000:
                await error(message, 'The react count must be an integer greater than 0 and less than 1000.')

            else:
                cursor.execute('''INSERT OR REPLACE INTO config_settings(guild_id, react_count) VALUES(?,?)''', (message.guild.id, react_count_config))
                db.commit()

                emb = discord.Embed(
                    description='React count has been set to {}'.format(str(react_count_config)),
                    color=0x7289da,
                    title='Confirmation'
                )
                await message.channel.send(embed=emb)

        if message.content == str('+lastpin'):
            channelPins = await message.channel.pins()
            if not channelPins:
                await error(message, 'There are no pinned messages in #{}'.format(message.channel))
                return
            lastPin = channelPins[0]
            pinned_name = lastPin.author.display_name
            pinned_avatar = lastPin.author.avatar_url
            pinned_content = lastPin.content
            attachments = lastPin.attachments
            server = message.guild.id

            # Description is the contents of the first pinned message
            emb = discord.Embed(description=pinned_content, color=0x7289da)
            # Match author information from pinned message
            emb.set_author(
                name=pinned_name,
                icon_url=pinned_avatar,
                url='https://discordapp.com/channels/{0}/{1}/{2}'.format(
                    server, lastPin.channel.id, lastPin.id))

            # Handle attachments in pins
            if message.attachments:
                img_url = message.attachments[0].url
                emb.set_image(url=img_url)

            await message.channel.send(embed=emb)

        if message.content == '+status':
            emb = discord.Embed(description='Online.', color=0x7289da)
            await message.channel.send(embed=emb)

        if message.content == '+stats' and message.author.id == 357652932377837589:
            num_servers = len(client.guilds)
            server_names = []
            total_members = 0
            for server in client.guilds:
                if server.id != 264445053596991498:
                    server_names.append(server.name)
                    total_members += len(server.members)
            emb = discord.Embed(
            description='**Servers:** {0} \n **Users:** {1}'.format(str(num_servers), str(total_members)),
            color=0x7289da,
            title='Statistics'
            )
            await message.channel.send(embed=emb)

        if message.content.startswith('+archive'):
            # See above
            if not await message_read_perms(message):
                await invalid_perms(message)
                return
            try:
                # Extract the message ID
                id_to_archive = message.content.replace('+archive ', '')
                msg = await message.channel.fetch_message(id_to_archive)

                if str('pin-archive') not in await available_channels(message):
                    await on_guild_join(message.guild)
                    await asyncio.sleep(1)

                if str('pin-archive') in await available_channels(message):
                    await archive_message(msg)
                    await asyncio.sleep(10)
                    await message.delete()

            # If this exception is thrown, it usually means we had an invalid message ID.
            except discord.errors.HTTPException as e:
                emb = discord.Embed(
                    description='Error: Message not found in #{}, try again.'.format(message.channel),
                    color=0x7289da)
                await message.channel.send(embed=emb)

        if message.content == '+help':
            try:
                help_message = '''
           __**Commands**__:

            **1)** Last Pinned Message:
            Usage: +lastpin
            Purpose: Displays the last pinned message of the current channel.

            **2)** Archive Messages (Manual)
            Usage: +archive <messageid>
            Permission: Must have a role with the manage_messages permission.
            Purpose: To archive a message to #pin-archive, regardless whether the message is pinned.

            **3)** Status:
            Usage: +status
            Purpose: Notifies the user if the bot is online.

            **4** React Count:
            Usage: +setreactcount <integer>
            Permission: Must be an administrator/guild owner or have the manage_messages permission.
            Purpose: Set the count for which '📌' reacts will pin a message, default value is {}
          '''.format(7)
                emb = discord.Embed(description=help_message, color=0x7289da)
                await message.channel.send(embed=emb)

            except:
                await error(message, 'Pin Archiver does not have permission to send messages in {}'.format(message.channel))


def try_config(config, heading, key):
    """Attempt to extract config[heading][key], with error handling.

    This function wraps config access with a try-catch to print out informative
    error messages and then exit."""
    try:
        section = config[heading]
    except KeyError:
        print("Missing config section [{}]".format(heading))
        sys.exit(1)

    try:
        value = section[key]
    except KeyError:
        print("Missing config key '{}' under section '[{}]'".format(
            key, heading))
        sys.exit(1)
    return value

if __name__ == "__main__":
    # Parse command-line arguments for the token and the config file path.
    # It uses a positional argument for the token and a flag -c/--config to
    # specify the path to the config file.
    parser = argparse.ArgumentParser()
    #parser.add_argument("token")
    parser.add_argument(
        "-c", "--config", help="Config file path", default="config.ini")
    args = parser.parse_args()

    # Parse the config file at the given path, erroring out if keys are missing
    # in the config.
    config = configparser.ConfigParser()
    config.read(args.config)
    try:
        TOKEN = try_config(config, "IDs", "Token")
    except KeyError:
        sys.exit(1)

    client.run(TOKEN)
cursor.close()
db.close()
