![pinArchiver Banner](https://i.imgur.com/OhpJKc1.jpg)
# Discord Pin Archiver Bot
Pin Archiver is a Discord bot that was specifically made for the [Discord server](https://discord.gg/ZZFJhdr) of the alumni ran [Subreddit](https://www.reddit.com/r/uwaterloo/) for the University of Waterloo; however, since then, the bot has been made open source for the public to use. 

If you require assistance in any means regardng the bot, feel free to join the [Pin Archiver Support Server](https://discord.gg/jY9xADW), or, [click here to invite](https://discordapp.com/oauth2/authorize?client_id=533383387763965982&permissions=268823632&scope=bot) the bot to your server (hosted by me).

Pin Archiver has the following features:
- Archives pinned messages to an archive channel, this message is an embed which:
  - Displays the author of the message and their profile picture.
  - Displays the channel in which the message was sent in.
  - A hyper-link to jump to the chat location of the message.
- Allows channels to exceed the maximum pin limit (50), by deleting the oldest pinned message once the maximum has been reached.
- Creates an archive channel named 'pin-archive' upon joining the server if one hasn't been found upon pinning a message or when the bot joins the server.
- Pins (and archives) a message if it receives 7 '📌' reactions.
- When pinning a message in an private channel, the user will be given the option to pin the message but not archive it.
- Fetch the last pinned message in the current channel (+lastpin).
- Archive any message, regardless of whether it was pinned, via the message id (e.g +archive 615697286105923639).
- Fetch a list of the bot's commands mentioned above, along with required permissions and examples (+help). 

## Usage
`+lastpin`: Displays the last pinned message of the current channel. 

`+archive`: Archives a message to #pin-archive regardless of whether the message is pinned. 

`+status`: Notifies the user if the bot is online

`+help`: Displays all of the bots commands, including the permissions required to execute.

Note: +archive requires the user to have the manage messages permission. Guild owners or users with administrator permissions will have access to this as well.

## To-do
I have lots of plans for the future regarding this bot! Here are some of the features I plan on implementing:
* Configuration system via a web interface similar to Mee6, ideally, guild administrators would be able to login to a website with their Discord account and configure the bot to their liking. This includes changing permissions for commands, the archive channel name, the reaction emoji and/or its required reacts to pin, disable warning messages and more. 


## Operation
Requirements:

   discord.py
   Python 3.6x 

If you plan on hosting the bot yourself, clone the repository via `git clone -b master https://github.com/HaiderZaidiDev/Discord-Pin-Archiver-Bot master` and run the main.py file. If you still want the bot to run after you close your SSH session I suggest setting up a screen to keep the file running in a background session. 

I have tested and used this on Ubuntu 16.04 LTS, however, I recommend using something like 18.04 LTS so you don't have to go through the troubles of getting Python 3.6 working on it. 


   

