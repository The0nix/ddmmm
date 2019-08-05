#!/usr/bin/env python3
import os
import pickle
import logging

import discord
from valve.source import NoResponseError

from utils import TOKEN, CHANNELS_DIR, get_players, get_players_info

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s] %(message)s')
logger = logging.getLogger(__name__)

HELP_MESSAGE = \
"""Available commands:
!online - show number of players on the server
!players - show names of players on the server
!sub - subscribe channel to players join notifications
!sub - unsubscribe channel from players join notifications
!help - show this help message"""

client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!players'):
        try:
            player_count, players = await get_players_info()
        except NoResponseError:
            msg = 'Couldn\'t reach the server'
        else:
            msg = '{} {} online:\n{}'.format(
                    player_count, 
                    'player' if player_count % 10 == 1 else 'players',
                    '\n'.join(players)
                )
        await client.send_message(message.channel, msg)
    elif message.content.startswith('!online'):
        try:
            player_count, max_players = await get_players()
        except NoResponseError:
            msg = 'Couldn\'t reach the server'
        else:
            msg = '{}/{} players online'.format(player_count, max_players)
        await client.send_message(message.channel, msg)
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
