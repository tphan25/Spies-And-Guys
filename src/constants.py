class RequestType:
    HELP = 'help'
    INIT_LOBBY = 'init_lobby'
    START_GAME = 'start_game'
    START_ROUND = 'start_round'
    END_ROUND = 'end_round'
    PLAYERS = 'players'
    ADD_PLAYER = 'add_player'
    ADD_PLAYERS = 'add_players'
    REMOVE_PLAYER = 'remove_player'
   
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
