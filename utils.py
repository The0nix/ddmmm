import os

from valve.source import a2s, NoResponseError
from valve.source.messages import BrokenMessageError

SEPARATOR = ','

TOKEN = os.environ['DDMMM_TOKEN']
SERVER_NAMES = os.environ['DDMMM_SERVER_NAMES'].split(SEPARATOR)
SERVER_IPS = os.environ['DDMMM_SERVER_IPS'].split(SEPARATOR)
SERVER_PORTS = [int(port) for port in os.environ['DDMMM_SERVER_PORTS'].split(SEPARATOR)]
assert len(SERVER_IPS) == len(SERVER_PORTS) == len(SERVER_NAMES)
SERVERS = list(zip(SERVER_NAMES, SERVER_IPS, SERVER_PORTS))

CHANNELS_DIR = 'channels'


async def get_players():
    counts = []
    for _, ip, port in SERVERS:
        with a2s.ServerQuerier((ip, port)) as server:
            try:
                info = server.info()
            except (NoResponseError, BrokenMessageError):
                info = {'player_count': None, 'max_players': None}
            counts.append((info['player_count'], info['max_players']))
    return counts


async def get_players_info():
    players_info = []
    for ip, port in zip(SERVER_IPS, SERVER_PORTS):
        with a2s.ServerQuerier((ip, port)) as server:
            try:
                players = server.players()
            except (NoResponseError, BrokenMessageError):
                players = {'player_count': None, 'players': []}
            players_info.append((players['player_count'],
                                [player['name'] for player in players['players']]))
    return players_info
