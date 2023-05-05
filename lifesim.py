import random

from metaclass import Map, Sector
from playerclass import Player, Alliance
# from rulesets import ...

class Game():
	def __init__(self, rule):
		self.rule = rule
		self.players = []
		self.alliances = []
		self.map = None