import math
import random

from functools import reduce

class Player():
    def __init__(self, index, name, lives):
        self.index = index
        self.name = name
        self.lives = lives
        self.alliance = None
        self.hostile = False

    def setLives(self, lives):
        self.lives = lives

    def getIndex(self):
        return self.index

    def getName(self):
        return self.name
    
    def getLives(self):
        return self.lives
    
    def setAlliance(self, alliance):
        self.alliance = alliance
    
    def getAlliance(self):
        return self.alliance
    
    def getAllianceName(self):
        return self.alliance.getName()

    def setHostile(self, hostile):
        self.hostile = hostile

    def isHostile(self):
        return self.hostile
    
    def leaveAlliance(self):
        if (self.alliance != None):
            self.alliance.removeMember(self)
            if self.alliance.disband():
                self.alliance = None
                return True
            self.alliance = None
        return False
    
    @staticmethod
    def getNameString(players):
        if len(players) == 1:
            return players[0].getName()
        # last = players.pop()
        def combine(x, y):
            return x + ", " + y
        playStr = map(lambda x: x.getName(), players[:-1])
        return reduce(combine, playStr) + " and " + players[-1].getName()


class Alliance():
    def __init__(self, name, members):
        self.name = name
        self.members = members
        self.stength = random.randint(1,3)

    def getName(self):
        return self.name

    def getMembers(self):
        return self.members

    def removeMember(self, p):
        self.members.remove(p)
    
    def getStrength(self):
        return self.strength
    
    def disband(self):
        if len(self.getMembers()) < 1 or random.randrange(0, len(self.getMembers())**2) == 0:
            for p in self.members:
                p.setAlliance(None)
            print("{alliance} has disbanded...".format(alliance = self.name))
            return True
        return False
    
    @staticmethod
    def getAllianceBonus(p1, p2):
        return p1.getAlliance().getStrength() if p1.getAlliance() == p2.getAlliance else 0
