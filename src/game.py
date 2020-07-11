"""
This module manages the actual game logic of Spies and Guys.
The game itself may function on any platform (web, discord, mobile)
using these rules/framework.
"""
from typing import List
import math
import random

# Maps that we store to help in determining how many spies
# and guys there are, and squadsizes, and # of fails
# required.
MAP_FAILNEEDS_TO_COUNT = {
    5: [1, 1, 1, 1, 1],
    6: [1, 1, 1, 1, 1],
    7: [1, 1, 1, 2, 1],
    8: [1, 1, 1, 2, 1],
    9: [1, 1, 1, 2, 1],
    10: [1, 1, 1, 2, 1],
}

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

class InvalidLobbyPhaseError(ValueError):
    """
    Error describing when an event occurs but the lobby phase
    does not match with the event, and thus action cannot be
    made.
    """
    def __init__(self, msg):
        self.msg = msg


class InvalidCommandError(ValueError):
    """
    Error describing an invalid command type from the user. Example
    would be a user trying to perform an action of another role.
    """
    def __init__(self, msg):
        self.msg = msg


class PlayerRole:
    """
    Class enum which contains different types of roles of the players.
    None is before assignment, while spies are assigned when the lobby
    is initialized.
    """
    NONE = 'none'
    SPY = 'spy'
    GUY = 'guy'

class PreparationVote:
    """
    Class enum containing different types of votes. By default users
    have NOVOTE, but during voting phase they may choose to use either
    of the other types of votes.
    """
    NOVOTE = 'VOTE_NOVOTE'
    REJECT = 'REJECT'
    ACCEPT = 'ACCEPT'

class MissionVote:
    """
    Class enum containing different types of mission votes. These
    determine whether a mission succeeds or fails, and should only be usable
    by the squad on the mission.
    """
    NOVOTE = 'MISSION_NOVOTE'
    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'

class Player():
    """
    A player model. They have a name and role, and different types of votes
    for different purposes outlined above.
    """
    def __init__(self, name: str):
        self.name = name
        self.role = PlayerRole.NONE
        self.vote = PreparationVote.NOVOTE
        self.mission_vote = MissionVote.NOVOTE

    def __eq__(self, other: Player) -> bool:
        return self.name == other.name and self.role == other.role and self.vote == other.vote

    def set_vote(self, vote: PreparationVote) -> None:
        """
        Set the player's preparation vote to the specified vote.
        """
        self.vote = vote

    def set_mission_vote(self, mission_vote: MissionVote) -> None:
        """
        Set the player's mission vote to the specified vote.
        """
        self.mission_vote = mission_vote


# Enum class for different Game Statuses
class GameStatus:
    """
    Class enum representing different types of game statuses.
    Depending on the phase of the lobby/game, this should be altered
    and certain actions should be enabled/disabled as a result.
    """
    NOT_RUNNING = 'NOT RUNNING'
    IN_LOBBY = 'IN_LOBBY'
    PREPARING_TEAMS = 'PREPARING_TEAMS'
    PREPARING_MISSION = 'PREPARING_MISSION'
    VOTING_PHASE = 'VOTING_PHASE'
    PERFORMING_MISSION = 'PERFORMING_MISSION'
    GAME_OVER_SPY_VICTORY = 'GAME_OVER_SPY_VICTORY'
    GAME_OVER_GUY_VICTORY = 'GAME_OVER_GUY_VICTORY'

# Class storing an entire game with players.
class Game():
    """
    Class representing an entire game with players. Each game has its own
    isolated state, containing players and a state including the phase of the game,
    different state variables, and more.
    """
    def __init__(self):
        self.lobby = []
        self.state = GameStatus.NOT_RUNNING
        self.round_number = 1
        self.captain_index = 0
        self.squad = []
        self.preparation_vote_count = 0
        self.mission_vote_count = 0
        self.failed_mission_count = 0

    def init_lobby(self):
        """
        Initializes the lobby. Functions only if lobby is NOT_RUNNING
        or it throws an error; then sets the state of the lobby to start accepting
        players.
        Expected phase: NOT_RUNNING -> IN_LOBBY
        """
        if self.state != GameStatus.NOT_RUNNING:
            raise InvalidLobbyPhaseError(f'Cannot initialize lobby in this phase'\
                    '(currently {self.state}')
        self.state = GameStatus.IN_LOBBY

    def start_game(self) -> None:
        """
        Starts the game. Functions only if lobby is IN_LOBBY.
        Sets the game state to GameStatus.PREPARING_TEAMS and
        assigns x number of players to be spies, where x is
        the number of spies corresponding to size of lobby.
        Changes from IN_LOBBY to PREPARING_TEAMS.
        """
        if self.state != GameStatus.IN_LOBBY:
            raise InvalidLobbyPhaseError(f'Cannot start game in this phase'\
                    '(currently {self.state})')
        self.state = GameStatus.PREPARING_TEAMS
        lobby_length = len(self.lobby)
        if lobby_length < 5:
            raise InvalidLobbyPhaseError(f'{len(self.lobby)} players in the lobby.'\
                    'Need at least 5 to start.')
        spy_count = MAP_SPYCOUNT_TO_COUNT[lobby_length]
        spy_indices = set([])
        while len(spy_indices) < spy_count:
            index = math.floor(int(random.random() * lobby_length))
            if not index in spy_indices:
                spy_indices.add(index)
        for index in range(len(self.lobby)):
            if index in spy_indices:
                self.lobby[index].role = PlayerRole.SPY
            else:
                self.lobby[index].role = PlayerRole.GUY

    def captain_choose_squad(self, players: List[Player]):
        """
        Captain chooses the squad. Only the captain themselves
        can trigger this action; we change phase from
        PREPARING_MISSION to VOTING_PHASE as a result.
        """
        pass

    def handle_vote(self, player: Player, vote: PreparationVote) -> None:
        """
        Handles a single player vote during the VOTING_PHASE.
        It sets that player's vote so that they cannot vote
        again. Once the voting limit is reached, we change phase
        to either PERFORMING_MISSION or PREPARING_MISSION again
        based on vote results.
        """
        player.set_vote(vote)
        self.preparation_vote_count += 1
        if self.preparation_vote_count == len(self.lobby):
            vote_accepted = self.check_preparation_votes()
            if vote_accepted:
                self.state = GameStatus.PERFORMING_MISSION
            else:
                self.state = GameStatus.PREPARING_MISSION
            self.clear_votes()

    # Handle a vote from a player; once we hit capacity, check if the mission
    # is a failure.
    # Expected Phase: PERFORMING_MISSION -> GAME_OVER or PREPARING_MISSION
    def handle_mission_vote(self, player: Player, mission_vote: MissionVote):
        """
        Handles a vote from a player on the assigned squad.
        It sets that player's mission_vote so they cannot vote again.
        Once the voting limit is reached, we change phase to either GAME_OVER_X_WIN
        or PREPARING_MISSION based on vote results.
        """
        player.set_mission_vote(mission_vote)
        self.mission_vote_count += 1
        if self.mission_vote_count == len(self.squad):
            is_success = self.check_mission_votes()
            if not is_success:
                self.failed_mission_count += 1
                if self.failed_mission_count == 3:
                    self.state = GameStatus.GAME_OVER_SPY_VICTORY
            self.round_number += 1
            if self.round_number - self.failed_mission_count == 3:
                self.state = GameStatus.GAME_OVER_GUY_VICTORY

    def add_player(self, player: Player):
        """
        Add a single player to the lobby.
        """
        if player in self.lobby:
            raise InvalidCommandError('Player is already in lobby. Please use another name.')
        self.lobby.append(player)

    def get_player(self, name: str):
        """
        Returns a player by name. Generally should be used as a utility.
        """
        for player in self.lobby:
            if player.name == name:
                return player
        return None

    # Checks votes. Set the next phase of the game depending on result of vote.
    # If majority (or tie with captain voting for one team) accepts, return True.
    def check_preparation_votes(self) -> bool:
        """
        Checks the preparation votes to see whether the
        mission was accepted or failed. Generally goes to majority, but
        if a tie occurs, should go to the captain's voting side.
        """
        captain_vote = None
        accepts = 0
        for i, player in enumerate(self.lobby):
            if i == self.captain_index:
                captain_vote = player.vote
            if player.vote == PreparationVote.ACCEPT:
                accepts += 1
        return accepts > len(self.lobby) / 2 or \
            (accepts == len(self.lobby) / 2 and captain_vote == PreparationVote.ACCEPT)

    # Clears votes in lobby by setting them to NOVOTE and resetting vote count.
    def clear_votes(self) -> None:
        """
        Cleans up player votes back to NOVOTE.
        """
        for player in self.lobby:
            player.set_vote(PreparationVote.NOVOTE)
        self.preparation_vote_count = 0

    def check_mission_votes(self):
        """
        Checks the mission votes to see whether the mission succeeded
        or failed. Depends on MAP_FAIL_NEEDS_TO_COUNT.
        """
        required_votes = MAP_FAIL_NEEDS_TO_COUNT[len(self.lobby)]
        current_fail_votes = 0
        for player in self.squad:
            if player.mission_vote == MissionVote.FAIL:
                current_fail_votes += 1
            if current_fail_votes >= required_votes:
                return False
        return True



    def print_players(self):
        """
        Prints out the players; generally a utility func
        """
        for player in self.lobby:
            print(f'{player.name} is a {player.role}')
