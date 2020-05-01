from constants import PlayerRoles

class Player:
    def __init__(self, name):
        self.name = name
        self.role = PlayerRoles.GUY

    def __eq__(self, other):
        return self.name == other.name and self.role == other.role
