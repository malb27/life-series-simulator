"""
Game map and associated elements.
"""

import random

from gameElements import Trap

class Map():
    """
    Representation of the world map.
    Map 'shrinks' to force players to always be in close proximity.
    """
    def __init__(self, numsectors):
        self.numsectors = numsectors
        self.sectors = []
        for _ in range(0, numsectors):
            self.sectors.append(Sector())

    def update_sectors(self, num):
        """Update amount of sectors and move traps as needed."""
        while num < self.numsectors:
            # Move the trap to a different sector
            trap = self.sectors.pop().get_trap()
            if trap:
                sec = random.choice(self.sectors)
                sec.add_trap(trap)
            self.numsectors -= 1

    def allocate_sector(self, players):
        """Allocate players to sectors randomly."""
        for sector in self.sectors:
            sector.clear_players()
        for player in players:
            self.sectors[random.randrange(0, self.numsectors)].add_player(player)
        return self.sectors

    def set_trap(self, player):
        """Set a new trap in a sector."""
        trap = Trap(player)
        sec = random.choice(self.sectors)
        sec.add_trap([trap])
        return trap.set_message()

class Sector():
    """
    Object representing a portion of the world map.
    """
    def __init__(self):
        self.players = []
        self.hostile = []
        self.trap = []

    def add_player(self, player):
        """Adds a player to the map sector, appending them to the correct list."""
        if player.is_hostile():
            self.hostile.insert(random.randint(0, len(self.hostile)),
                                player)
        self.players.insert(random.randint(0, len(self.players)),
                            player)

    def shuffle_players(self):
        """Randomly shuffles player order in the sector."""
        random.shuffle(self.players)

    def clear_players(self):
        """Removes all players from the sector."""
        self.players = []
        self.hostile = []

    def get_players(self):
        """Get non-hostile players in the sector."""
        return self.players

    def get_hostile(self):
        """Get hostile players in the sector."""
        return self.hostile

    def get_trap(self):
        """Get the active trap."""
        return self.trap

    def get_trap_setter(self):
        """Get the player who set the trap in the current sector."""
        if len(self.trap) > 0:
            return self.trap[0].get_player()
        else:
            return None

    def add_trap(self, trap):
        """Adds a new trap to the sector."""
        self.trap += trap
        random.shuffle(self.trap)

    def trigger_trap(self, num, tripped):
        """Activates a trap."""
        trap = self.trap.pop(0)
        return trap.trigger(num, tripped)
