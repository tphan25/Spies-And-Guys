from game_globals import LOBBY_LIST
from random import random
from constants import PlayerRoles

def assign_roles(spy_count: int):
    global LOBBY_LIST
    count = 0
    spy_indices = []
    while count < spy_count:
        index = int(random() * (len(LOBBY_LIST) - 1))
        if not index in spy_indices:
            spy_indices.append(index)
            count += 1
    for index in spy_indices:
        LOBBY_LIST[index].role = PlayerRoles.SPY

def reset_roles():
    global LOBBY_LIST
    for player in LOBBY_LIST:
        player.role = PlayerRoles.GUY

def print_players():
    global LOBBY_LIST
    for player in LOBBY_LIST:
        print(f'{player.name} is a {player.role}')

def setup_fake_lobby():
    global LOBBY_LIST
    for name in ['Tam', 'Jacob', 'Kenny', 'Jedediah', 'Anakin', 'Veronica', 'Annie', 'Jessica']:
        LOBBY_LIST.append(Player(name))
