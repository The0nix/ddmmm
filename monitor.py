#!/usr/bin/env python3
import asyncio
import os
import logging
import pickle
import time

import discord
from valve.source import NoResponseError
from valve.source.messages import BrokenMessageError

from utils import TOKEN, CHANNELS_DIR, get_players_info

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s] %(message)s')
logger = logging.getLogger(__name__)

client = discord.Client()

current_players_names = set()


async def send_stats():
    with open('data.pickle', 'rb') as f:
        channel = pickle.load(f)
    msg = 'check!'
    await client.send_message(channel, msg)


async def check_players(send=True):
    global current_players_names
    try:
        player_count, players_names = await get_players_info()
    except NoResponseError:
        logger.warning('Couldn\'t connect to server')
        return
    except BrokenMessageError:
        logger.error('BrokenMessageError')
        return
    players_names = set(players_names)
    if send and players_names != current_players_names:
        new_players = players_names - current_players_names
        gone_players = current_players_names - players_names
        if new_players or gone_players:
            new_players_msg = \
                '{} joined the server\n{} currently playing'.format(','.join(new_players), player_count)
            gone_players_msg = \
                '{} left the server\n{} currently playing'.format(','.join(gone_players), player_count)
            for channel_filename in os.listdir(CHANNELS_DIR):
                with open(os.path.join(CHANNELS_DIR, channel_filename), 'rb') as f:
                    channel = pickle.load(f)
                if new_players:
                    await client.send_message(channel, new_players_msg)
                if gone_players:
                    await client.send_message(channel, gone_players_msg)
    current_players_names = players_names

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    logger.info('Starting bot')
    loop.run_until_complete(client.login(TOKEN))
    logger.info('Starting notifications monitoring')
    loop.run_until_complete(check_players(send=False))
    try:
        while True:
            loop.run_until_complete(check_players())
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info('Closing due to keyboard interrupt')
    finally:
        loop.run_until_complete(client.logout())
        loop.close()
