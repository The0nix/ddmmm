#!/usr/bin/env python3
import asyncio
import logging
import os
import pickle
import time

import discord

from utils import TOKEN, CHANNELS_DIR, SERVER_NAMES, get_players_info

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s] %(message)s')
logger = logging.getLogger(__name__)

client = discord.Client()

current_players_names = {name: set() for name in SERVER_NAMES}


async def send_stats():
    with open('data.pickle', 'rb') as f:
        channel = pickle.load(f)
    msg = 'check!'
    await client.send_message(channel, msg)


async def check_players(send=True):
    global current_players_names
    for server_name, (player_count, players_names) in zip(SERVER_NAMES, await get_players_info()):
        if player_count is None:
            logger.info('Couldn\'t connect to server')
            continue
        players_names = set(players_names)
        if send and players_names != current_players_names[server_name]:
            new_players = players_names - current_players_names[server_name]
            gone_players = current_players_names[server_name] - players_names
            if new_players or gone_players:
                new_players_msg = '{} joined {}\n{} currently playing'.format(', '.join(new_players),
                                                                              server_name,
                                                                              player_count)
                gone_players_msg = '{} left {}\n{} currently playing'.format(', '.join(gone_players),
                                                                             server_name,
                                                                             player_count)
                for channel_filename in os.listdir(CHANNELS_DIR):
                    with open(os.path.join(CHANNELS_DIR, channel_filename), 'rb') as f:
                        channel = pickle.load(f)
                    if new_players:
                        await client.send_message(channel, new_players_msg)
                    if gone_players:
                        await client.send_message(channel, gone_players_msg)
        current_players_names[server_name] = players_names

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
