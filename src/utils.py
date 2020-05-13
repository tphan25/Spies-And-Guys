from game_globals import LOBBY_LIST
from random import random
from constants import PlayerRoles, MAP_SPYCOUNT_TO_COUNT

def assign_roles():
    global LOBBY_LIST
    spy_count = get_num_spies(len(LOBBY_LIST)) 
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

def get_num_spies(lobby_size):
    return MAP_SPYCOUNT_TO_COUNT.get(lobby_size)
