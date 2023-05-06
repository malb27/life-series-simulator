import random

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

    def setHostile(self, hostile):
        self.hostile = hostile

    def isHostile(self):
        return self.hostile
        

class Alliance():
    def __init__(self, members):
        self.members = members
        self.stength = random.randint(1,3)

    def getMembers(self):
        return self.members
    
    def getStrength(self):
        return self.strength
    
    def disband(self):
        for p in self.members:
            p.setAlliance(None)
    
    @staticmethod
    def getAllianceBonus(p1, p2):
        return p1.getAlliance().getStrength() if p1.getAlliance() == p2.getAlliance else 0
