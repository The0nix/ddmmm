import os

from valve.source import a2s


TOKEN = os.environ['DDMMM_TOKEN']
SERVER_IP = os.environ['DDMMM_SERVER_IP']
SERVER_PORT = int(os.environ['DDMMM_SERVER_PORT'])

CHANNELS_DIR = 'channels'


async def get_players():
    with a2s.ServerQuerier((SERVER_IP, SERVER_PORT)) as server:
        info = server.info()
        player_count = info['player_count']
        max_players = info['max_players']
        return player_count, max_players


async def get_players_info():
    with a2s.ServerQuerier((SERVER_IP, SERVER_PORT)) as server:
        players = server.players()
        player_count = players['player_count']
        players_names = [player['name'] for player in players['players']]
        return player_count, players_names
