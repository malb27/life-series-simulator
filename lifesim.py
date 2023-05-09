from random import randint, choice, choices
from math import ceil, floor

from gameMap import Map
from playerManagement import Player, Alliance
from rulesets import ThirdLife
from signallers import sig

HOURS = 3
REL_CAP = 5

class Game():
    def __init__(self):
        self.rule = None
        self.players = []
        self.eliminated = []
        self.alliances = []
        self.map = None
        self.relationships = []
        self.session = 0

    def init(self):
        self.map = Map(ceil(len(self.players)/2))
        self.relationships = [None] * len(self.players)
        for i in range(len(self.players)):
            self.relationships[i] = [0] * len(self.players)

    def addPlayer(self, name): # Add support for stats later
        player = Player(len(self.players), name, self.rule.setLives())
        self.players.append(player)

    def setRules(self,rule):
        self.rule = rule

    def getRelationship(self, p1, p2):
        # Add boogey penalty later
        rel = self.relationships[p1.getIndex()][p2.getIndex()] + Alliance.getAllianceBonus(p1,p2)
        # Actual alliance value can go over -5/5, but returned value is hard capped
        return min(REL_CAP, rel) if rel > 0 else max(-REL_CAP, rel)
    
    # Randomly decay relationships - move values closer to 0
    def decayRelationships(self):
        for i, p in enumerate(self.relationships):
            for j in range(0, len(p)):
                val = self.relationships[i][j]
                self.relationships[i][j] -= int(val/abs(val)) if val != 0 and randint(0,1) == 0 else 0
    
    def playerElimination(self, p):
        sig.playerEliminated(p)
        self.players.remove(p)
        self.eliminated.insert(0, p)
        a = p.getAlliance()
        if (p.leaveAlliance(self.relationships)): # Alliance has disbanded
            self.alliances.remove(a)

    def generateConflictSides(self, a, d, players):
        players.remove(a)
        players.remove(d)
        
        if len(players) == 0: # Only 2 players in combat, no need to assign sides
            self.relationships[a.getIndex()][d.getIndex()] -= randint(0,1)
            sig.playerFight([a], [d])
            return [a], [d]

        attackers = [a]
        defenders = [d]

        for p in players:
            arel = self.getRelationship(p, a)
            drel = self.getRelationship(p, d)
            if ((p.getAlliance() != None and p.getAlliance() == d.getAlliance()) 
                    or drel == REL_CAP or randint(0,REL_CAP-drel) == 0):
                defenders.append(p)
            elif p.isHostile() and (arel == REL_CAP or randint(0, REL_CAP-arel) == 0):
                attackers.append(p)

        for d in defenders:
            for a in attackers:
                self.relationships[d.getIndex()][a.getIndex()] -= randint(0,1)

        sig.playerFight(attackers, defenders)
        return attackers, defenders

    def battle(self, offence, defence):
        osum = []
        dsum = []
        for a in offence:
            osum.append(randint(0,10))
        for d in defence:
            dsum.append(randint(0,10))
        winning, losing = (defence, offence) if sum(osum) < sum(dsum) else (offence, defence)

        for p in losing:
            if randint(0, len(offence)) == 0:
                sig.playerEscape(p, winning)
            else:
                a = choice(winning)
                sig.playerKilled(p, a)                
                self.relationships[p.getIndex()][a.getIndex()] -= (randint(1,3) 
                    + (2 if p.getAlliance() != None and p.getAlliance() == d.getAlliance() 
                    else 0))
                if (self.rule.playerKill(p, a)):
                    self.playerElimination(p)
                a.incKills()

    def generateConflict(self, players, hostile):
        # For each hostile, RNG 0-5 + relation - lives - modifier affected by surviving players
        # If any land on 0, conflict - otherwise return False
        for h in hostile:
            for p in players:
                val = (0 if self.getRelationship(h, p) == -REL_CAP  
                       else randint(0, REL_CAP+self.getRelationship(h, p)) 
                       - p.getLives() 
                       - floor(8/len(self.players)))
                if val <= 0 and h.getIndex() != p.getIndex():
                    s1, s2 = self.generateConflictSides(h, p, players)
                    self.battle(s1, s2)
                    return True
        return False
    
    def generateSinglePlayerEvent(self, player):
        match randint(1,5):
            case 1:
                sig.playerDeath([player])
                if (self.rule.playerDeath(player)):
                    self.playerElimination(player)
            case _:
                sig.filler([player], [], [], self.session)

    def generateEvent(self, players):   
        def relationUpdate(s1, s2, sign, amount):
            for p1 in s2:
                for p2 in s1:
                    i1, i2 = p1.getIndex(), p2.getIndex()
                    self.relationships[i1][i2] += sign*randint(amount[0],amount[1])
                    if sign > 0:
                        self.relationships[i2][i1] += randint(amount[0],amount[1])

        if len(players) == 1:
            self.generateSinglePlayerEvent(players[0])
            return

        # Ensures an alliance between ALL surviving players cannot be made.
        if (len(self.players) > len(players) and randint(0,HOURS-1) == 0
                and all(p.getAlliance() == None for p in players)):
            name = []
            for p in players:
                name.append(p.getName()[0])
            name = ''.join(name)
            sig.allianceCreate(players, name)

            ally = Alliance(name, players)
            for p in players:
                p.setAlliance(ally)
            self.alliances.append(ally)
            return
        
        # Push event generation to rulesets potentially in future?
        # Lots of repeated code even with template structure, tweaking will be difficult
        s1, s2 = self.generateSides(players)
        match randint(1,15):
            case f if 1 <= f <= 5:
                sig.filler(players, s1, s2, self.session)
            case n if n in [6,7]:
                sig.eventMinorPos(s1, s2)
                relationUpdate(s1, s2, 1, [1,2])
            case p if p in [8,9]:
                sig.eventMinorNeg(s1, s2)
                relationUpdate(s1, s2, -1, [1,2])
            case 10:
                sig.eventMajorPos(s1, s2)
                relationUpdate(s1, s2, 1, [3,4])
            case 11:
                sig.eventMajorNeg(s1, s2)
                relationUpdate(s1, s2, -1, [3,4])
            case d if 12 <= d <= 15:
                sig.playerDeath(s1)
                for p in s1:
                    if (self.rule.playerDeath(p)):
                        self.playerElimination(p)
                sig.filler(s2, s2, [], self.session)

    def runDay(self):
        self.session += 1
        self.map.updateSectors(ceil(len(self.players)/2))
        sig.gameNextSesh(self.session)
        for i in range(0, HOURS):
            if (self.runHour(self.map.allocateSector(self.players))):
                sig.statsWin(self.players[0])
                sig.cont()
                sig.statsEnd(self.players, self.eliminated)
                return True

        # Relationship Decay
        if self.session % 3:
            self.decayRelationships()    
        
        sig.cont()
        sig.stats(self.players, self.session)
        sig.cont()
        return False

    def runHour(self, sectors):
        for s in sectors:
            hostile = s.getHostile()
            players = s.getPlayers()
            if len(players) == 0: # No players in sector
                continue
            if len(hostile) > 0:
                if (self.generateConflict(players, hostile)):
                    if len(self.players) < 2:
                        return True
                    continue
            self.generateEvent(players)

        # There should always be 1 player left, but the check is present
        # incase something somehow goes wrong
        if len(self.players) < 2:
            return True

        # Check alliance stability
        for a in self.alliances:
            if (a.disband(self.relationships)):
                self.alliances.remove(a)

        return False
        
    @staticmethod
    def generateSides(players):
        playerSet = set(players)
        s1 = set(choices(players, k=randint(1, len(players)-1)))
        s2 = list(playerSet - s1)
        s1 = list(s1)
        return s1, s2
    
    # def start(self):
    #     print("\n-- STARTING LIVES --")
    #     for p in self.players:
    #         print("{name}: {n} lives".format(name = p.getName(), n = p.getLives()))


if __name__ == "__main__":
    game = Game()
    rule = ThirdLife(game)
    game.setRules(rule)
    sig.start()
    players = input("\nPlayers: ").split(", ") # Sanitise if frontend ever made

    # players = []
    # while (True):
    #     inp = input()
    #     if not inp:
    #         break
    #     players += inp.split(", ")
    
    for p in players:
        game.addPlayer(p)
    game.init()

    # game.start()

    while not game.runDay():
        continue