#!/usr/bin/env python3
import logging
import os
import pickle

import discord

from utils import TOKEN, CHANNELS_DIR, SERVER_NAMES, SERVER_IPS, SERVER_PORTS, get_players, get_players_info

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s] %(message)s')
logger = logging.getLogger(__name__)

HELP_MESSAGE = \
"""Available commands:
!online - show number of players on servers
!players - show names of players on servers
!ip - show IPs of servers
!sub - subscribe channel to players joining notifications
!unsub - unsubscribe channel from players joining notifications
!help - show this help message"""

client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!players'):
        msgs = []
        for server_name, (player_count, players) in zip(SERVER_NAMES, await get_players_info()):
            if player_count is None:
                msgs.append('Couldn\'t reach {}'.format(server_name))
            else:
                msgs.append('{}: {} {} online:\n{}'.format(
                        server_name,
                        player_count,
                        'player' if player_count % 10 == 1 else 'players',
                        '\n'.join(players)
                    ))
        await client.send_message(message.channel, ('\n'+'-'*30+'\n').join(msgs))
    elif message.content.startswith('!online'):
        msgs = []
        for server_name, (player_count, max_players) in zip(SERVER_NAMES, await get_players()):
            if player_count is None:
                msgs.append('Couldn\'t reach {}'.format(server_name))
            else:
                msgs.append('{}: {}/{} players online'.format(server_name, player_count, max_players))
        await client.send_message(message.channel, '\n'.join(msgs))
    elif message.content.startswith('!ip'):
        msgs = []
        for server_name, server_ip, server_port in zip(SERVER_NAMES, SERVER_IPS, SERVER_PORTS):
            msgs.append('{}:\t{}:{}'.format(server_name, server_ip, server_port))
        await client.send_message(message.channel, '\n'.join(msgs))
    elif message.content.startswith('!sub'):
        os.makedirs(CHANNELS_DIR, exist_ok=True)
        channel_path = os.path.join(CHANNELS_DIR, str(message.channel.id))
        if os.path.exists(channel_path):
            msg = 'This channel is already subscribed'
        else:
            msg = 'Subscribed channel to notifications'
        with open(channel_path, 'wb') as f:
            pickle.dump(message.channel, f)

        await client.send_message(message.channel, msg)
    elif message.content.startswith('!unsub'):
        try:
            os.remove(os.path.join(CHANNELS_DIR, str(message.channel.id)))
        except FileNotFoundError:
            msg = 'This channel was not subscribed in the first place'
        else:
            msg = 'Unsubscribed channel from notifications'
        await client.send_message(message.channel, msg)
    elif message.content.startswith('!help'):
        msg = HELP_MESSAGE
        await client.send_message(message.channel, msg)


@client.event
async def on_ready():
    logger.info('Logged in as')
    logger.info(client.user.name)
    logger.info(client.user.id)
    logger.info('------')

if __name__ == '__main__':
    client.run(TOKEN)
