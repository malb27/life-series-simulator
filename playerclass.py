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
        self.kills = 0

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
        return self.alliance.getName() if self.alliance != None else "None"

    def setHostile(self, hostile):
        self.hostile = hostile

    def isHostile(self):
        return self.hostile
    
    def getKills(self):
        return self.kills
    
    def incKills(self):
        self.kills += 1
    
    def leaveAlliance(self, relations):
        if (self.alliance != None):
            self.alliance.removeMember(self)
            if relations and self.alliance.disband(relations):
                self.alliance = None
                return True
            self.alliance = None
        return False
    
    # def leaveAlliance(self):
    #     if (self.alliance != None):
    #         self.alliance.removeMember(self)
    #         self.alliance = None
    
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

    def checkStability(self, relations):
        perceptions = [0] * len(self.members)
        individual = [0] * len(self.members)
        overall = 0
        for i, p in enumerate(self.members):
            for j, t in enumerate(self.members):
                rel = relations[p.getIndex()][t.getIndex()]
                individual[i] += rel
                perceptions[j] += rel
                overall += rel
        
        kicked = []
        leaving = []

        for i, val in enumerate(perceptions):
            if val <= -len(self.members):
                kicked.append(self.members[i])

        for i, val in enumerate(individual):
            if val < -len(self.members):
                leaving.append(self.members[i])

        for k in kicked:
            k.leaveAlliance([])
            print("{p} was kicked from {ally}.".format(p = k.getName(), ally = self.name))

        for i in leaving:
            i.leaveAlliance([])
            print("{p} has left {ally}.".format(p = i.getName(), ally = self.name))

        # print("{name}: {p}, {i}, {o}".format(name = self.name, p = perceptions, i = individual, o = overall))

        if overall < -len(self.members+kicked+leaving) or len(kicked + leaving) >= len(self.members):
            return True

        return False

    def disband(self, relations):
        if len(self.getMembers()) < 2 or self.checkStability(relations):
            for p in self.members:
                p.setAlliance(None)
            print("[?] {alliance} has fallen apart...".format(alliance = self.name))
            return True
        return False
    
    @staticmethod
    def getAllianceBonus(p1, p2):
        return p1.getAlliance().getStrength() if p1.getAlliance() == p2.getAlliance else 0
