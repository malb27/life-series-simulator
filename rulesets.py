from playerManagement import Player
from signallers import sig

class ThirdLife():
    def __init__(self, game):
        self.game = game

    def setLives(self):
        return 3
    
    def playerDeath(self, p):
        p.setLives(p.getLives() - 1)
        if p.getLives() == 0:
            return True
        if p.getLives() == 1:
            sig.playerRed(p)
            p.setHostile(True)
        return False
    
    def playerKill(self, p1):
        return self.playerDeath(p1)

    def assignBoogey():
        return

    # def giveLife(p1, p2):
    #     return
    
    # def endHour():
    #     return