"""
Rulesets for different life series.
"""

from signallers import sig

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
        p.set_lives(p.get_lives() - 1)
        if p.get_lives() == 0:
            return True
        if p.get_lives() == 1:
            sig.player_red(p)
            p.set_hostile(True)
        return False

    def player_kill(self, p1):
        """Handle player kills."""
        return self.player_death(p1)

    # def assignBoogey():
    #     return

    # def giveLife(p1, p2):
    #     return

    # def endHour():
    #     return
