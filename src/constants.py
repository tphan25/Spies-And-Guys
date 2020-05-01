class RequestType:
    HELP = 'help'
    INIT_LOBBY = 'init_lobby'
    START_GAME = 'start_game'
    END_ROUND = 'end_round'
    ADD_PLAYER = 'add_player'
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
