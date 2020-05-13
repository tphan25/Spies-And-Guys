from constants import RequestType, GameStatuses
from game_globals import LOBBY_LIST, GAME_STATUS, ROUND_NUMBER
from models import Player
from utils import (
    assign_roles,
    reset_roles,
    print_players
)
from random import random

async def action_help(message, msg_split):
    msg_to_send = 'Help was requested. Display some instructions here.'
    await message.channel.send(msg_to_send)

# Allows a user to initialize a lobby.
# Should create proper data structures and put the
# game into SETUP state.
async def action_init_lobby(message, msg_split):
    global GAME_STATUS
    msg_to_send = ('Lobby initialized. Please add players by entering "!sg add_player <name>" '
                   'or start the game by typing "!sg start_game".')
    GAME_STATUS = GameStatuses.IN_LOBBY
    await message.channel.send(msg_to_send)

# If all users are ready then it should begin the game.
# Should assign users Spy/Guy role and message them, and
# inform them of their partners if applicable.
async def action_start_game(message, msg_split):
    global LOBBY_LIST
    global GAME_STATUS
    if GAME_STATUS != GameStatuses.IN_LOBBY:
        await message.channel.send('Lobby was not initialized. Please initialize the lobby and add players.')
        return
    if len(LOBBY_LIST) < 5:
        await message.channel.send(f'{len(LOBBY_LIST)} players in the lobby. Need at least 5 to start.') 
        return
    assign_roles()
    # We check if users are PERFORMING_MISSION before allowing them to start a round
    GAME_STATUS = GameStatuses.PERFORMING_MISSION
    msg_to_send = ("Roles have been assigned and messages have been sent. "
                   "Please check your personal messages to see if you are "
                   "a spy, and find out who your fellow traitors are. ")
    await message.channel.send(msg_to_send)

async def action_start_round(message, msg_split):
    global ROUND_NUMBER
    global GAME_STATUS
    global LOBBY_LIST
    global CAPTAIN_INDEX
    if GAME_STATUS != GameStatuses.PERFORMING_MISSION:
        await message.channel.send(f'Cannot start the round as the game status is {GAME_STATUS}')
    ROUND_NUMBER += 1
    if ROUND_NUMBER == 1:
        CAPTAIN_INDEX = int(random() * (len(LOBBY_LIST) - 1))
    msg_to_send = "Starting the round. The current captain is:\n"
    for index, player in enumerate(LOBBY_LIST):
        if index == CAPTAIN_INDEX:
            msg_to_send += ">"
        else:
            msg_to_send += " "
        msg_to_send += f'{player.name}\n'
    await message.channel.send(msg_to_send)

# Should allow for users to request the bot to end the round
# and any debate, and finalize team members aboard.
async def action_end_round(message, msg_split):
    msg_to_send = 'Player asked to end_round. End round and move on'
    await message.channel.send(msg_to_send)

# Lists out the current players in the lobby.
# Also gives the current captain name if possible.
async def action_list_players(message, msg_split):
    global LOBBY_LIST
    global GAME_STATUS
    global CAPTAIN_INDEX
    msg_to_send = "List of players:\n"
    if GAME_STATUS == GameStatuses.PREPARING_MISSION or GAME_STATUS == GameStatuses.PERFORMING_MISSION:
        msg_to_send += f'The captain is: {LOBBY_LIST[CAPTAIN_INDEX]}\n'
    for player in LOBBY_LIST:
        msg_to_send += f'{player.name}\n'
    await message.channel.send(msg_to_send)

# Should allow for users to add a player to the list. They can specify
# a name or we will default to their discord username.
async def action_add_player(message, msg_split):
    global LOBBY_LIST
    if GAME_STATUS != GameStatuses.IN_LOBBY:
        await message.channel.send('Cannot add players at this time.')
        return
    if len(msg_split) > 2:
        player_name = msg_split[2]
        msg_to_send = f'{player_name} added to lobby.'
        player = Player(player_name)
        if player in LOBBY_LIST:
            await message.channel.send('Player is already in lobby. Please use another name.')
            return
        LOBBY_LIST.append(Player(player_name))
        await message.channel.send(msg_to_send)
    else:
        await message.channel.send('You need to specify a player to add.')

async def action_add_players(message, msg_split):
    global LOBBY_LIST
    if GAME_STATUS != GameStatuses.IN_LOBBY:
        await message.channel.send('Cannot add players at this time.')
        return
    if len(msg_split) > 2:
        player_names = msg_split[2:]
        players_added = []
        players_not_added = []
        for player_name in player_names:
            player = Player(player_name.strip(','))
            if player in LOBBY_LIST:
                players_not_added.append(player)
            else:
                players_added.append(player)
        LOBBY_LIST += players_added

        msg_to_send = "Players added:\n"
        if len(players_added) == 0:
            msg_to_send += "None\n"
        for player in players_added:
            msg_to_send += f'{player.name}\n'

        msg_to_send += "Players not added:\n"
        if len(players_not_added) == 0:
            msg_to_send += "None\n"
        for player in players_not_added:
            msg_to_send += f'{player.name}\n'
        await message.channel.send(msg_to_send)
    else:
        await message.channel.send('You need to specify players to add.')

# Attempts to remove a player from the current lobby.
# If the player is not in the lobby it will return a message saying
# player does not exist.
async def action_remove_player(message, msg_split):
    global LOBBY_LIST
    if GAME_STATUS != GameStatuses.IN_LOBBY:
        await message.channel.send('Cannot add players at this time.')
        return
    if len(msg_split) > 2:
        player_name = msg_split[2]
        msg_to_send = f'{player_name} was removed from the lobby.'
        try:
            LOBBY_LIST.remove(Player(player_name))
        except ValueError:
            msg_to_send = f'{player_name} was not found in the lobby.'
        await message.channel.send(msg_to_send)
    else:
        await message.channel.send('You need to specify a player to remove.')


ACTIONS = {
    RequestType.HELP: action_help,
    RequestType.INIT_LOBBY: action_init_lobby,
    RequestType.START_GAME: action_start_game,
    RequestType.START_ROUND: action_start_round,
    RequestType.END_ROUND: action_end_round,
    RequestType.PLAYERS: action_list_players,
    RequestType.ADD_PLAYER: action_add_player,
    RequestType.ADD_PLAYERS: action_add_players,
    RequestType.REMOVE_PLAYER: action_remove_player,
}
