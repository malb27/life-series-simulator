import random

class Player():
    def __init__(self, index, name, lives):
        self.index = index
        self.name = name
        self.lives = lives
        self.alliance = None
        self.hostile = False

    def getIndex(self):
        return self.index

    def getName(self):
        return self.name
    
    def getLives(self):
        return self.lives
    
    def getAlliance(self):
        return self.alliance

    def isHostile(self):
        return self.hostile
        

class Alliance():
    def __init__(self, members, strength):
        self.members = members
        self.stength = strength

    def getMembers(self):
        return self.members
    
    def getStrength(self):
        return self.strength
