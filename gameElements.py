"""
Auxillery game components that aren't pivotal to its function.
"""

from random import choice, randint

from gameMessages.trapTypes import TYPES

MAX_STEALTH = 7
MAX_LETHAL = 7

class Trap():
    """
    Class for traps that are set by players.
    """
    def __init__(self, player):
        self.player = player # Who set it?
        self.type = choice(TYPES) # Type of trap
        self.stealth = randint(3, MAX_STEALTH) # How hidden is the trap
        self.lethality = randint(3, MAX_LETHAL) # How lethal is it

    def set_message(self):
        """Return the message set used by this trap."""
        return self.type["set"]

    def get_player(self):
        """Get the player who set this trap."""
        return self.player

    def trigger(self, num, tripped):
        """Trigger the trap."""
        if not tripped:
            if num >= MAX_STEALTH or randint(num, MAX_STEALTH) > self.stealth:
                return False, self.type["disarm"], self.player
            if num >= MAX_LETHAL or randint(num, MAX_LETHAL) > self.lethality:
                return False, self.type["escape"], self.player
        return True, self.type["kill"], self.player
