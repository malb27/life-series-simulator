import math
import random

from functools import reduce

from metaclass import Map, Sector
from playerclass import Player, Alliance
from rulesets import ThirdLife

HOURS = 3

class Game():
    def __init__(self):
        self.rule = None
        self.players = []
        self.alliances = []
        self.map = None
        self.relationships = []
        self.session = 0

    def init(self):
        self.map = Map(math.ceil(len(self.players)/2))
        self.relationships = [None] * len(self.players)
        for i in range(len(self.players)):
            self.relationships[i] = [0] * len(self.players)

    def addPlayer(self, name): # Add support for stats later
        player = Player(len(self.players), name, self.rule.setLives())
        self.players.append(player)

    def addAlliance(self, players):
        alliance = Alliance(players, random.randint(1,4))
        self.alliances.append(alliance)

    def setRules(self,rule):
        self.rule = rule

    def setRelationship(self, p1, p2, val):
        if val < -5:
            self.relationships[p1.getIndex()][p2.getIndex()] = -5
        elif val > 5:
            self.relationships[p1.getIndex()][p2.getIndex()] = 5
        else:
            self.relationships[p1.getIndex()][p2.getIndex()] = val

    def getRelationship(self, p1, p2):
        # add boogey penalty later
        return self.relationships[p1.getIndex()][p2.getIndex()] + Alliance.getAllianceBonus(p1,p2)

    def generateSides(self, a, d, players):
        players.remove(a)
        players.remove(d)
        attackers = [a]
        defenders = [d]
        if len(players) == 0:
            return attackers, defenders

        for p in players:
            if p.getAlliance() == d.getAlliance() or random.randint(0,5-self.relationships[p.getIndex()][d.getIndex()]) == 0:
                print("{defender} rushes in to defend {player}!".format(defender = p.getName(), player = d.getName()))
                defenders.append(p)

        return attackers, defenders

    def battle(self, offence, defence):
        osum = []
        dsum = []
        for a in offence:
            osum.append(random.randint(0,10))
        for d in defence:
            dsum.append(random.randint(0,10))
        winning, losing = (defence, offence) if sum(osum) < sum(dsum) else (offence, defence)

        for p in losing:
            if random.randint(0, len(offence)) == 0:
                print("{player} barely escapes with their life".format(player = p.getName()))
                pass
            else:
                a = random.choice(winning)
                print("{player} was slain by {attacker}".format(player = p.getName(), attacker = a.getName()))
                self.setRelationship(p, a, self.relationships[p.getIndex()][a.getIndex()]-random.randint(1,3))
                if (self.rule.playerKill(p, a)):
                    print("{player} has been eliminated!".format(player = p.getName()))
                    self.players.remove(p)

    def generateConflict(self, players, hostile):
        # For each hostile, RNG 0-5 + relation with each opponent
        # If any land on 0, conflict - otherwise return False
        for h in hostile:
            for p in players:
                val = random.randint(0, 5+(self.relationships[h.getIndex()][p.getIndex()]))
                if val == 0 and h.getIndex() != p.getIndex():
                    print("{attacker} attacks {defender}!".format(attacker = h.getName(), defender = p.getName()))
                    s1, s2 = self.generateSides(h, p, players)
                    self.battle(s1, s2)
                    return True
        return False

    def generateEvent(self, players):
        def test(x, y):
            return x + ", " + y
        
        if len(players) > 1 and random.randrange(0,HOURS-1) == 0 and all(p.getAlliance() == None for p in players):
            playStr = map(lambda x: x.getName(), players)
            print(reduce(test, playStr), "have made an alliance!")
            ally = Alliance(players)
            for p in players:
                p.setAlliance(ally)
            return
        # lambda x, y: x.getName() + ", " + y.getName()
        # Stub
        rand = random.randint(1,10)
        match rand:
            case 1:
                pass

        if len(self.players) > 3 and random.randint(0, 3) == 0:
            # rocks fall everyone dies
            for p in players:
                print("{player} fell out of the world".format(player = p.getName()))
                if (self.rule.playerDeath(p)):
                    print("{player} has been eliminated!".format(player = p.getName()))

                    self.players.remove(p)

    def runDay(self):
        self.session += 1
        self.map.updateSectors(math.ceil(len(self.players)/2))
        print("Session {num}".format(num = self.session))
        for i in range(0, HOURS):
            if (self.runHour(self.map.allocateSector(self.players))):
                print("Game End: Winner is {player}".format(player = self.players[0].getName()))
                return True
        return False

    def runHour(self, sectors):
        for s in sectors:
            hostile = s.getHostile()
            players = s.getPlayers()
            if len(hostile) > 0:
                if (self.generateConflict(players, hostile)):
                    continue
            self.generateEvent(players)
        if len(self.players) < 2:
            return True
        return False

if __name__ == "__main__":
    game = Game()
    rule = ThirdLife(game)
    game.setRules(rule)
    players = input("Players: ").split(" ")
    for p in players:
        game.addPlayer(p)
    game.init()
    while not game.runDay():
        continue