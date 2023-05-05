import random

class Map():
	def __init__(self, numsectors):
		self.numsectors = numsectors
		self.sectors = []
		for i in range(0, numsectors):
			self.sectors.append(Sector())
		# self.bases = []

	def allocateSector(self, players):
		for s in self.sectors:
			s.clearPlayers()
		for p in players:
			self.sectors[random.randrange(0, self.numsectors)].addPlayer(p)

class Sector():
	def __init__(self):
		# self.biome = None
		self.players = []
		self.hostile = []

	def addPlayer(self, player):
		self.players.append(player)
		if player.isHostile():
			self.hostile.append(player)

	def clearPlayers(self):
		self.players = []
		self.hostile = []

	def getPlayers(self):
		return self.players