import argparse
import configparser
import discord
import sys
import asyncio
from ast import literal_eval

client = discord.Client()
config = None
ARCHIVE_CHANNEL = None
SERVER = None
SUPER_ROLES = None
SUPER_USERS = None
REACTION_EMOJI = None
REACTION_COUNT = None
TOKEN = None


@client.event
async def on_ready():
    """Print a startup message."""
    print(str(client.user) + ' is online.')  # Prints operational message.
    await client.change_presence(activity=discord.Game(name='v1.0 | +help'))

@client.event
async def on_message_edit(before, after):
    """Main function for handling message edit events."""
    channelPins = await before.channel.pins()
    pinned_ids = [message.id for message in channelPins]
    attachments = after.attachments

    if len(pinned_ids) == 50:
        oldest_pin = await after.channel.fetch_message(pinned_ids[-1])
        await unpin(oldest_pin)

    if after.pinned and after.author != client.user:
        name = after.author.display_name
        avatar = after.author.avatar_url
        pin_content = after.content

        emb = discord.Embed(
            description=pin_content,
            color=0x7289da)  # Initalizes embed with description pin_content.
        emb.set_author(
            name=name,
            icon_url=avatar,
            url='https://discordapp.com/channels/{0}/{1}/{2}'.format(
                SERVER, after.channel.id, after.id)
        )  # Sets author and avatar url of the author of pinned message.

        # Set attachemnt image url as embed image if it exists
        if attachments:
            img_url = attachments[0]['url']
            emb.set_image(url=img_url)

        # Sets footer as the channel the message was sent and pinned in.
        emb.set_footer(text='Sent in #{}'.format(after.channel))

        # Finally send the message to the pin archiving channel.
        channel = client.get_channel(ARCHIVE_CHANNEL)
        await channel.send(embed=emb)

@client.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == REACTION_EMOJI:
        if reaction.count == REACTION_COUNT:
            await pin(reaction.message)

def check_super_perms(message):
    """Check that the message came from a user with "super" permissions.

    See config file [Perms]."""
    has_super_role = any(
        True for role in message.author.roles if role.name in SUPER_ROLES)
    return message.author.id in SUPER_USERS or has_super_role


@client.event
async def on_message(message):
    """Handle commands."""
    # If the message is not from a bot, the following code is executed.
    if message.author != client.user:
        if message.content == str('+lastpin'):
            channelPins = await message.channel.pins()
            lastPin = channelPins[0]
            pinned_name = lastPin.author.display_name 
            pinned_avatar = lastPin.author.avatar_url 
            pinned_content = lastPin.content
            attachments = lastPin.attachments

            # Description is the contents of the first pinned message
            emb = discord.Embed(description=pinned_content, color=0x7289da)
            # Match author information from pinned message
            emb.set_author(
                name=pinned_name,
                icon_url=pinned_avatar,
                url='https://discordapp.com/channels/{0}/{1}/{2}'.format(
                    SERVER, lastPin.channel.id, lastPin.id))

            # Handle attachments in pins
            if attachments:
                print(attachments)
                img_content = attachments[0]['url']
                emb.set_image(url=img_content)

            await message.channel.send(embed=emb)

        if message.content == '+status':
            emb = discord.Embed(description='Online.', color=0x7289da)
            await message.channel.send(embed=emb)

        if message.content.startswith('+del'):
            if not check_super_perms(message):
                return

            # Fetch the last message in the channel #pin-archive and delete
            channel = client.get_channel(ARCHIVE_CHANNEL)
            async for message in channel.history(limit=1):
                last_message = message
            await last_message.delete()

        if message.content.startswith('+archive'):
            # See above
            if not check_super_perms(message):
                return
            try:
                # Extract the message ID
                id_to_archive = message.content.replace('+archive ', '')
                msg = await message.channel.fetch_message(id_to_archive)
                attachments = msg.attachments

                name = msg.author.display_name
                avatar = msg.author.avatar_url
                pinned_content = msg.content

                emb = discord.Embed(description=pinned_content, color=0x7289da)
                emb.set_author(
                    name=name,
                    icon_url=avatar,
                    url='https://discordapp.com/channels/{0}/{1}/{2}'.format(
                        SERVER, msg.channel.id, msg.id))

                # Handle attachments
                if attachments:
                    img_content = attachments[0]['url']
                    emb.set_image(url=img_content)

                emb.set_footer(text='Sent in #{}'.format(msg.channel))
                channel = client.get_channel(ARCHIVE_CHANNEL)
                await channel.send(embed=emb)
                await asyncio.sleep(10)
                await message.delete()

            # If this exception is thrown, it usually means we had an
            # invalid message ID.
            except discord.errors.HTTPException as e:
                emb = discord.Embed(
                    description='Error: Message not found in #{}, try again.'.format(message.channel),
                    color=0x7289da)
                await message.channel.send(embed=emb)

        if message.content.startswith('+help'):
            help_message = '''
       __**Information**__:

        This bot was made by @Nitr0us#5090, if you have any questions or require support please contact him.

       __**Features**__:

        **1)** Last Pinned Message:
        Usage: +lastpin
        Purpose: Displays the last pinned message of the current channel.

        **2)** Archive Pinned Messages (Automatic):
        Usage: Automatic
        Usage Alternate: Culminate {0} pin reactions on a message.
        Purpose: To archive all pinned messages to #pin-archive.

        **3)** Archive Messages (Manual)
        Usage: +archive <messageid>
        Permission: Administrators & Moderators
        Purpose: To archive a message to #pin-archive, regardless whether the message is pinned.

        **4)** Status:
        Usage: +status
        Purpose: Notifies the user if the bot is online.
        
        **5)** Delete:
        Usage: +del
        Permission: Administrators & Moderators
        Purpose: To delete the last message in #pin-archive.
      '''.format(REACTION_COUNT)
            emb = discord.Embed(description=help_message, color=0x7289da)
            await message.channel.send(embed=emb)


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
        ARCHIVE_CHANNEL = int(try_config(config, "IDs", "ArchiveChannel"))
        SERVER = try_config(config, "IDs", "Server")
        SUPER_ROLES = literal_eval(try_config(config, "Perms", "SuperRoles"))
        SUPER_USERS = literal_eval(try_config(config, "Perms", "SuperUsers"))
        REACTION_EMOJI = try_config(config, "Reacts", "Emoji")
        REACTION_COUNT = int(literal_eval(try_config(config, "Reacts", "Count")))
        TOKEN = try_config(config, "IDs", "Token")
    except KeyError:
        sys.exit(1)

    client.run(TOKEN)
