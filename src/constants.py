class RequestType:
    # Management actions
    HELP = 'help'
    INIT_LOBBY = 'init_lobby'
    START_GAME = 'start_game'
    START_ROUND = 'start_round'
    END_ROUND = 'end_round'
    # Player actions
    PLAYERS = 'players'
    ADD_PLAYER = 'add_player'
    ADD_PLAYERS = 'add_players'
    REMOVE_PLAYER = 'remove_player'
    # In game actions
    SELECT_SQUAD = 'select_squad'
   
class GameStatuses:
    IN_LOBBY = 'in_lobby'
    PREPARING_TEAMS = 'preparing_teams'
    PREPARING_MISSION = 'preparing_mission'
    PERFORMING_MISSION = 'performing_mission'
    NOT_RUNNING = 'not_running'

class PlayerRoles:
    SPY = 'spy'
    GUY = 'guy'

MAP_SPYCOUNT_TO_COUNT = {
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    9: 3,
    10: 4,
}

MAP_SQUADSIZE_TO_COUNT = {
    5: [2, 3, 2, 3, 3],
    6: [2, 3, 4, 3, 4],
    7: [2, 3, 3, 4, 4],
    8: [3, 4, 4, 5, 5],
    9: [3, 4, 4, 5, 5],
    10: [3, 4, 4, 5, 5],
}

MAP_FAILNEEDS_TO_COUNT = {
    5: [1, 1, 1, 1, 1],
    6: [1, 1, 1, 1, 1],
    7: [1, 1, 1, 2, 1],
    8: [1, 1, 1, 2, 1],
    9: [1, 1, 1, 2, 1],
    10: [1, 1, 1, 2, 1],
}