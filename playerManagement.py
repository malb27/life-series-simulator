"""
Classes for players and player-related attributes.
"""
from math import ceil

from signallers import sig

REL_CAP = 10

class Player():
    """Player object."""
    def __init__(self, index, name, lives):
        self.index = index
        self.name = name
        self.lives = lives
        self.alliance = None
        self.hostile = False
        self.kills = 0

    def set_lives(self, lives):
        self.lives = lives

    def get_index(self):
        return self.index

    def get_name(self):
        return self.name

    def get_lives(self):
        return self.lives

    def set_alliance(self, alliance):
        self.alliance = alliance
        if alliance:
            alliance.add_member(self)

    def get_alliance(self):
        return self.alliance

    def get_alliance_name(self):
        """Get the name of the player's alliance."""
        return self.alliance.getName() if self.alliance is not None else "None"

    def set_hostile(self, hostile):
        self.hostile = hostile

    def is_hostile(self):
        return self.hostile

    def get_kills(self):
        return self.kills

    def inc_kills(self):
        """Incrememnt the number of kills."""
        self.kills += 1

    def leave_alliance(self, relations):
        """Makes the player leave their current alliance."""
        if self.alliance is not None:
            self.alliance.remove_member(self)
            if relations and self.alliance.disband(relations):
                self.alliance = None
                return True
            self.alliance = None
        return False


class Alliance():
    """Alliance object."""
    def __init__(self, name):
        self.name = name
        self.members = []
        self.strength = 1

    def get_name(self):
        return self.name

    def get_members(self):
        return self.members

    def add_member(self, p):
        self.members.append(p)

    def remove_member(self, p):
        self.members.remove(p)

    def get_strength(self):
        return self.strength

    def check_stability(self, relations):
        """
        Check alliance stability.
        Members will leave/be kicked if relationship is too low. If overall relationships
        are low, alliance will fall apart.
        """
        
        overall = 0

        while True:
            perceptions = [0] * len(self.members)
            individual = [0] * len(self.members)
            overall = 0

            for i, player in enumerate(self.members):
                for j, target in enumerate(self.members):
                    rel = relations[player.get_index()][target.get_index()]
                    #individual[i] += rel
                    perceptions[j] += rel
                    #overall += rel

            kicked = []
            leaving = []

            for i, val in enumerate(perceptions):
                if val <= -1.5*len(self.members):
                    kicked.append(self.members[i])

            for k in kicked:
                k.leave_alliance([])
                sig.alliance_kick(k, self.name)

            for i, player in enumerate(self.members):
                for j, target in enumerate(self.members):
                    rel = relations[player.get_index()][target.get_index()]
                    individual[i] += rel
                    #perceptions[j] += rel
                    overall += rel

            for i, val in enumerate(individual):
                if val < -1.5*len(self.members) and self.members[i] not in kicked:
                    leaving.append(self.members[i])

            for i in leaving:
                i.leave_alliance([])
                sig.alliance_leave(i, self.name)

            if len(kicked) == 0 and len(leaving) == 0:
                break

            if len(self.members) <= 1:
                return True

        if overall < -2*len(self.members):
            return True
        
        new_str = ceil(overall/REL_CAP)*2+1
        self.strength = new_str if new_str > 0 else 0

        return False

    def disband(self, relations):
        """Check if an alliance should be disbanded."""
        if len(self.get_members()) < 2 or self.check_stability(relations):
            for p in self.members:
                p.set_alliance(None)
            sig.alliance_disband(self.name)
            return True
        return False

    @staticmethod
    def get_alliance_bonus(p1, p2):
        """Get relationship bonus from being in the same alliance."""
        return (p1.get_alliance().get_strength()
                if p1.get_alliance() == p2.get_alliance else 0)
