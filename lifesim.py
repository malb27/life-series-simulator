import random

from metaclass import Map, Sector
from playerclass import Player, Alliance
# from rulesets import ...

HOURS = 3

class Game():
    def __init__(self, rule):
        self.rule = rule
        self.players = []
        self.alliances = []
        self.map = None
        self.relationships = []

    def init(self):
        self.map = Map()
        self.relationships = [None] * len(self.players)
        for i in range(len(self.players)):
            self.relationships[i] = [0] * len(self.players)

    def addPlayer(self, name): # Add support for stats later
        player = Player(len(self.players), name, self.rule.getLives())
        self.players.append(player)

    def addAlliance(self, players):
        alliance = Alliance(players, random.randrange(1,4))
        self.alliances.append(alliance)

    def generateSides(self, p1, p2, players):
        return [], []

    def battle(self, side1, side2):
        pass

    def generateConflict(self, players, hostile):
        # For each hostile, RNG 0-5 + relation with each opponent
        # If any land on 0, conflict - otherwise return False
        for h in hostile:
            for p in players:
                val = random.randrange(0, 5+(self.relationships[h.getIndex][p.getIndex]))
                if val == 0 and h.getIndex != p.getIndex:
                    s1, s2 = self.generateSides(h, p, players)
                    self.battle(s1, s2)
                    return True
        return False

    def generateEvent(self, players):
        pass

    def runDay(self):
        for i in range(0, HOURS):
            self.runHour(self.map.allocateSector(self.players))

    def runHour(self, sectors):
        for s in sectors:
            hostile = s.getHostile()
            players = s.getPlayers()
            if len(hostile) > 0:
                if (self.generateConflict(players, hostile)):
                    continue
            self.generateEvent(players)