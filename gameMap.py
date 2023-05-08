import random

class Map():
    def __init__(self, numsectors):
        self.numsectors = numsectors
        self.sectors = []
        for i in range(0, numsectors):
            self.sectors.append(Sector())
		# self.bases = []

    def updateSectors(self, num):
        while (num < self.numsectors):
            self.sectors.pop()
            self.numsectors -= 1

    def allocateSector(self, players):
        for s in self.sectors:
            s.clearPlayers()
        for p in players:
            self.sectors[random.randrange(0, self.numsectors)].addPlayer(p)
        return self.sectors

class Sector():
    def __init__(self):
        self.players = []
        self.hostile = []

    def addPlayer(self, player):
        if player.isHostile():
            self.hostile.insert(random.randint(0, len(self.hostile)), 
                                player) if len(self.hostile) > 0 else self.hostile.append(player)
        self.players.insert(random.randint(0, len(self.players)), 
                            player) if len(self.players) > 0 else self.players.append(player)

    def shufflePlayers(self):
        random.shuffle(self.players)

    def clearPlayers(self):
        self.players = []
        self.hostile = []

    def getPlayers(self):
        return self.players
        
    def getHostile(self):
        return self.hostile