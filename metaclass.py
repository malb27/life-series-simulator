import random

class Map():
	def __init__(self, sects):
		self.sectors = []
		for i in range(0, sects):
			self.sectors.append(Sector())
		self.bases = []

class Sector():
	def __init__(self):
		self.biome = None
		self.players = []