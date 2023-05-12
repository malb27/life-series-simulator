from random import choice, randint

from gameMessages.trapTypes import TYPES

from playerManagement import Player

MAX_STEALTH = 7
MAX_LETHAL = 7

class Trap():
    def __init__(self, player):
        self.player = player # Who set it?
        self.type = choice(TYPES) # Type of trap
        self.stealth = randint(0, MAX_STEALTH) # How hidden is the trap
        self.lethality = randint(0, MAX_LETHAL) # How lethal is it

    def setMessage(self):
        return self.type["set"]
    
    def getPlayer(self):
        return self.player

    def trigger(self, n, tripped):
        if not tripped:
            if randint(n, MAX_STEALTH) > self.stealth:
                return False, self.type["disarm"], self.player
            elif randint(n, MAX_LETHAL) > self.lethality:
                return False, self.type["escape"], self.player
        return True, self.type["kill"], self.player