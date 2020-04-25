from constants import RequestType

ACTIONS = {
    RequestType.HELP:

def action_help():
    pass

# Allows a user to initialize a lobby.
# Should create proper data structures and put the
# game into SETUP state.
def action_init_lobby():
    pass

# If all users are ready then it should begin the game.
# Should assign users Spy/Guy role and message them, and
# inform them of their partners if applicable.
def action_start_game():
    pass


def action_end():
    pass

