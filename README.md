![pinArchiver Banner](https://i.imgur.com/OhpJKc1.jpg)
# Discord Pin Archiver Bot
Pin Archiver is a Discord bot that was specifically made for the [Discord server](https://discord.gg/ZZFJhdr) of the alumni ran [Subreddit](https://www.reddit.com/r/uwaterloo/) for the University of Waterloo; however, since then, the bot has been made open source for the public to use. 

Note: This bot is still a work in progress as I have many plans and ideas to implement for the future (refer to to-do list) - I eventually plan on hosting the bot for the public to use once it is complete (will provide an invitiation link once that happens); however, if you wish to use the bot in the meantime feel free to host it yourself or make any edits you wish (refer to operation section). 

Pin Archiver has the following features:
* Fetch the last pinned message of the current channel.
* Archive all pinned messages in the server to a specified channel.
* Pin a message in the current channel if it recieves a certain number of reactions.
* Archive any message to a specified channel via the message id.
* Delete the last message from a specified channel.
* Delete the oldest pinned message in the channel once the maximum number of pinned messages has been reached.
* Creates an archive channel on server join, sets channel permissions to deny sending of messages. 
* Asks user for archive confirmation when pinning a message in a private-text-channel (ability to pin a message but not archive it). 

## Usage
`+lastpin`: Displays the last pinned message of the current channel. 

`+archive`: Archives a message to #pin-archive regardless of whether the message is pinned. 

`+status`: Notifies the user if the bot is online

`+del`: Deletes the last message in #pin-archive.

`+help`: Displays all of the bots commands, including the permissions required to execute.

* Note: +Archive and +Del can only be used by the super users or roles in the config.ini 

## To-do
I have lots of plans for the future regarding this bot! Here are some of the features I plan on implementing:
* Configuration system via a web interface similar to Mee6, ideally, guild administrators would be able to login to a website with their Discord account and configure the bot to their liking. This includes adding super users and roles, changing the reaction emoji, count, disable warning messages and more (pretty much everything in the configuration file plus a few more things). 


## Operation
Requirements:

   discord.py
   Python 3.6x 

If you plan on hosting the bot yourself, clone the repository via `git clone -b master https://github.com/HaiderZaidiDev/Discord-Pin-Archiver-Bot master` and run the main.py file. If you still want the bot to run after you close your SSH session I suggest setting up a screen to keep the file running in a background session. 

I have tested and used this on Ubuntu 16.04 LTS, however, I recommend using something like 18.04 LTS so you don't have to go through the troubles of getting Python 3.6 working on it. 


   

