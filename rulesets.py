"""
Rulesets for different life series.
"""

from signallers import sig
from random import randint, choice

class ThirdLife():
    """
    Third Life ruleset.
    """
    def __init__(self, game):
        self.game = game

    def set_lives(self):
        """How many lives each player should have."""
        return 3

    def player_death(self, p):
        """Handle player death."""
        return self.player_reduce_lives(p, 1)
    
    def player_reduce_lives(self, p, n):
        p.set_lives(p.get_lives() - n)
        if p.get_lives() == 0:
            return True
        if p.get_lives() == 1:
            sig.player_red(p)
            p.set_hostile(True)
        return False

    def player_kill(self, p1):
        """Handle player kills."""
        return self.player_death(p1)

    def assign_boogey(self, players):
        return

    def give_life(self, p1, p2):
        return False


class LastLife():
    """
    Last Life ruleset.
    """
    def __init__(self, game):
        self.game = game

    def set_lives(self):
        """How many lives each player should have."""
        return randint(2,6)

    def player_death(self, p):
        """Handle player death."""
        return self.player_reduce_lives(p, 1)
    
    def player_reduce_lives(self, p, n):
        if n == 0:
            return
        p.set_lives(p.get_lives() - n)
        if p.get_lives() == 0:
            return True
        if p.get_lives() == 1:
            sig.player_red(p)
            p.set_hostile(True)
        return False

    def player_kill(self, p1):
        """Handle player kills."""
        return self.player_death(p1)
    
    def assign_boogey(self, players):
        if all(x.is_hostile() for x in players):
            return

        chance = 128
        while randint(1,128) <= chance:
            boogey = choice(players)
            if boogey.get_lives() != 1 and not boogey.is_boogey():
                boogey.set_boogey()
                sig.boogey_pick(boogey)
                chance //= 2

    def give_life(self, p1, p2):
        sig.life_trade(p1, p2)
        p1.set_lives(p1.get_lives() - 1)
        p2.set_lives(p2.get_lives() + 1)
        if not p2.is_boogey():
            p2.set_hostile(False)
        return True