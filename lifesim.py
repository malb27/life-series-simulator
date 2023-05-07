import math
import random

from metaclass import Map
from playerclass import Player, Alliance
from rulesets import ThirdLife
from signallers import Signaller

HOURS = 3
sig = Signaller()

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

    def setRules(self,rule):
        self.rule = rule

    def setRelationship(self, p1, p2, val):
        self.relationships[p1.getIndex()][p2.getIndex()] = val  

    def getRelationship(self, p1, p2):
        # add boogey penalty later
        rel = self.relationships[p1.getIndex()][p2.getIndex()] + Alliance.getAllianceBonus(p1,p2)
        return max(5, rel) if rel > 0 else min(-5, rel)
    
    def playerElimination(self, p):
        sig.playerEliminated(p.getName())
        self.players.remove(p)
        a = p.getAlliance()
        if (p.leaveAlliance()):
            self.alliances.remove(a)

    def generateConflictSides(self, a, d, players):
        players.remove(a)
        players.remove(d)
        attackers = [a]
        defenders = [d]
        if len(players) == 0:
            return attackers, defenders

        for p in players:
            arel = self.getRelationship(p, a)
            drel = self.getRelationship(p, d)
            if p.getAlliance() != None and p.getAlliance() == d.getAlliance():
                print("{defender} rushes in to defend their fellow {alliance} member, {player}!".format(defender = p.getName(), alliance = p.getAllianceName(), player = d.getName()))
                defenders.append(p)
            elif drel == 5 or random.randint(0,5-drel) == 0:
                print("{defender} jumps in to defend {player}!".format(defender = p.getName(), player = d.getName()))
                defenders.append(p)
            elif p.isHostile() and (arel == 5 or random.randint(0, 5-arel) == 0):
                print("{attacker} joins {player}!".format(attacker = p.getName(), player = a.getName()))
                attackers.append(p)

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
                print("[-] {player} was slain by {attacker}".format(player = p.getName(), attacker = a.getName()))
                self.setRelationship(p, a, self.relationships[p.getIndex()][a.getIndex()]-random.randint(1,3))
                if (self.rule.playerKill(p, a)):
                    self.playerElimination(p)

    def generateConflict(self, players, hostile):
        # For each hostile, RNG 0-5 + relation with each opponent
        # If any land on 0, conflict - otherwise return False
        for h in hostile:
            for p in players:
                val = 0 if self.getRelationship(h, p) == -5 else random.randint(0, 5+self.getRelationship(h, p))
                if val == 0 and h.getIndex() != p.getIndex():
                    print("{attacker} attacks {defender}!".format(attacker = h.getName(), defender = p.getName()))
                    s1, s2 = self.generateConflictSides(h, p, players)
                    self.battle(s1, s2)
                    return True
        return False
    
    def generateSinglePlayerEvent(self, player):
        match random.randint(1,10):
            case 1:
                pass
            case _:
                sig.filler([player], [], [], self.session)

    def generateEvent(self, players):    
        if len(players) == 1:
            self.generateSinglePlayerEvent(players[0])
            return

        if len(self.players) > len(players) and random.randrange(0,HOURS-1) == 0 and all(p.getAlliance() == None for p in players):
            name = []
            for p in players:
                name.append(p.getName()[0])
            name = ''.join(name)
            sig.allianceCreate(Player.getNameString(players), name)

            ally = Alliance(name, players)
            for p in players:
                p.setAlliance(ally)
            self.alliances.append(ally)
            return
        
        # Push event generation to rulesets potentially in future?
        # Lots of repeated code even with template structure, tweaking will be difficult
        s1, s2 = self.generateSides(players)
        match random.randint(1,10):
            case f if f in [1,8]:
                sig.filler(players, s1, s2, self.session)
            # case n if n in [4,5]:
            #     pass
            # case p if p in [6,7]:
            #     pass
            # case 8:
            #     pass
            # case 9:
            #     pass
            case d if d in [9,10]:
                sig.playerDeath(s1)
                for p in s1:
                    if (self.rule.playerDeath(p)):
                        self.playerElimination(p)
                sig.filler(s2, s2, [], self.session)

    def runDay(self):
        self.session += 1
        self.map.updateSectors(math.ceil(len(self.players)/2))
        print("\n. : Session {num} : .".format(num = self.session))
        for i in range(0, HOURS):
            # print(" ! Hour {num} !".format(num = i))
            if (self.runHour(self.map.allocateSector(self.players))):
                print("\n[ [ Game End: Winner is {player} ] ]".format(player = self.players[0].getName()))
                return True
        return False

    def runHour(self, sectors):
        for s in sectors:
            # print("----------------------------------")
            hostile = s.getHostile()
            players = s.getPlayers()
            # if (len(players) != 0):
            #     print(Player.getNameString(players))
            if len(players) == 0:
                continue
            if len(hostile) > 0:
                if (self.generateConflict(players, hostile)):
                    continue
            self.generateEvent(players)

        # > Alliance stability
        # > Relationship decay

        if len(self.players) < 2:
            return True
        return False
    
    @staticmethod
    def generateSides(players):
        playerSet = set(players)

        s1 = set(random.choices(players, k=random.randrange(1, len(players))))
        s2 = list(playerSet - s1)
        s1 = list(s1)

        return s1, s2

        # split = random.randrange(0, len(players))
        # return players[:split], players[split:]
        # sides = [[], []]
        # for p in players:
        #     sides[random.randrange(0, 2)].append(p)
        # return sides[0], sides[1]

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