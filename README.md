# Discord bot for monitoring Dark Messiah of Might & Magic server status

Bot link: https://discordapp.com/api/oauth2/authorize?client_id=607554062463795201&permissions=2048&scope=bot

## Available commands
The bot currently supports following commands:
* !online - show number of players on the server
* !players - show names of players on the server
* !sub - subscribe channel to players joininig notifications
* !unsub - unsubscribe channel from players joining notifications
* !help - show help message

Once you subscribed a channel, the bot will send notifications about players joining and leaving the server

## Requirements
This project requires python3 < 3.7 because of backwards incompatible asyncio changes in python 3.7

## Usage
The bot consists of two parts: `bot.py` which launches the bot and allows it to reply to commands and `monitor.py` which sends notificatoins to subscribed channel when players join or leave the server.
To launch the bot you must first set the following environment variables:
* `DDMMM_TOKEN` — Discord bot token
* `DDMMM_SERVER_IP` — Dark Messiah server ip
* `DDMMM_SERVER_PORT` — Dark Messiah server port

Then you run both `bot.py` and `monitor.py` files
