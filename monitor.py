#!/usr/bin/env python3
import asyncio
import os
import logging
import pickle
import time

import discord
from valve.source import NoResponseError, a2s
from valve.source.messages import BrokenMessageError

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s] %(message)s')
logger = logging.getLogger(__name__)

CHANNELS_DIR = 'channels'

TOKEN = os.environ['DDMMM_TOKEN']
SERVER_IP = os.environ['DDMMM_SERVER_IP']
SERVER_PORT = int(os.environ['DDMMM_SERVER_PORT'])

client = discord.Client()

current_players_names = set()


async def get_players_info():
    with a2s.ServerQuerier((SERVER_IP, SERVER_PORT)) as server:
        players = server.players()
        player_count = players['player_count']
        players_names = [player['name'] for player in players['players']]
    return player_count, players_names


async def send_stats():
    with open('data.pickle', 'rb') as f:
        channel = pickle.load(f)
    msg = 'check!'
    await client.send_message(channel, msg)


async def check_players():
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
    if players_names != current_players_names:
        new_players = players_names - current_players_names
        gone_players = current_players_names - players_names
        current_players_names = players_names
        if new_players or gone_players:
            new_players_msg = \
                'Players joined the server: {}\n{} currently playing'.format(','.join(new_players), player_count)
            gone_players_msg = \
                'Players left the server: {}\n{} currently playing'.format(','.join(gone_players),player_count)
            for channel_filename in os.listdir(CHANNELS_DIR):
                with open(os.path.join(CHANNELS_DIR, channel_filename), 'rb') as f:
                    channel = pickle.load(f)
                if new_players:
                    await client.send_message(channel, new_players_msg)
                if gone_players:
                    await client.send_message(channel, gone_players_msg)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    logger.info('Starting bot')
    loop.run_until_complete(client.login(TOKEN))
    logger.info('Starting notifications monitoring')
    try:
        while True:
            loop.run_until_complete(check_players())
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info('Closing due to keyboard interrupt')
    finally:
        loop.run_until_complete(client.logout())
        loop.close()
