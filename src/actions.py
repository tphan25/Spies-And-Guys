from constants import RequestType, GameStatuses
from game_globals import LOBBY_LIST, GAME_STATUS
from models import Player

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
    msg_to_send = 'Player asked to start_game. Set up and assign roles'
    await message.channel.send(msg_to_send)

# Should allow for users to request the bot to end the round
# and any debate, and finalize team members aboard.
async def action_end_round(message, msg_split):
    msg_to_send = 'Player asked to end_round. End round and move on'
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
    RequestType.END_ROUND: action_end_round,
    RequestType.ADD_PLAYER: action_add_player,
    RequestType.REMOVE_PLAYER: action_remove_player,
}
