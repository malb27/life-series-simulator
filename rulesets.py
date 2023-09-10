"""
Rulesets for different life series.
"""

from signallers import sig
from random import randint, choice

class ThirdLife():
    """
    Third Life ruleset.
    """
    def __init__(self, game):
        self.game = game
    
    def start(self, players):
        pass

    def set_lives(self):
        """How many lives each player should have."""
        return 3

    def player_death(self, p):
        """Handle player death."""
        return self.player_reduce_lives(p, 1)
    
    def player_reduce_lives(self, p, n):
        p.set_lives(p.get_lives() - n)
        if p.get_lives() == 0:
            return True
        if p.get_lives() == 1:
            sig.player_red(p)
            p.set_hostile(True)
        return False

    def player_kill(self, p1):
        """Handle player kills."""
        return self.player_death(p1)

    def assign_boogey(self, players):
        return

    def give_life(self, p1, p2):
        return False
    
    def assign_soulmates(self, players):
        return players

    def can_ally(self, players):
        return True


class LastLife():
    """
    Last Life ruleset.
    """
    def __init__(self, game):
        self.game = game

    def start(self, players):
        sig.lives(players)
        sig.cont()

    def set_lives(self):
        """How many lives each player should have."""
        return randint(2,6)

    def player_death(self, p):
        """Handle player death."""
        return self.player_reduce_lives(p, 1)
    
    def player_reduce_lives(self, p, n):
        if n == 0:
            return
        p.set_lives(p.get_lives() - n)
        if p.get_lives() == 0:
            return True
        if p.get_lives() == 1:
            sig.player_red(p)
            alliance = p.get_alliance()
            if alliance != None:
                sig.alliance_leave(p, alliance.get_name())
                p.leave_alliance([])
            p.set_hostile(True)
        return False

    def player_kill(self, p1):
        """Handle player kills."""
        return self.player_death(p1)
    
    def assign_boogey(self, players):
        if all(x.is_hostile() for x in players) or len(list(filter(lambda x: x.get_lives() > 1, players))) < 2:
            return

        chance = len(players)//2 + 1
        base = chance
        while randint(1,base) <= chance:
            boogey = choice(players)
            if boogey.get_lives() != 1 and not boogey.is_boogey():
                boogey.set_boogey()
                sig.boogey_pick(boogey)
                chance = (chance/5) * 3

    def give_life(self, p1, p2):
        sig.life_trade(p1, p2)
        p1.set_lives(p1.get_lives() - 1)
        p2.set_lives(p2.get_lives() + 1)
        if not p2.is_boogey():
            p2.set_hostile(False)
        # push alliance leaving sig to alliance itself
        if p2.get_lives() == 2 and p2.get_alliance() != None:
                sig.alliance_leave(p2, p2.get_alliance().get_name())
                p2.leave_alliance(self.game.get_relationships())
        return True
    
    def assign_soulmates(self, players):
        return players
    
    def can_ally(self, players):
        return all(p.get_lives() == 1 for p in players) or all(p.get_lives() != 1 for p in players) 
    
class DoubleLife():
    """
    Double Life ruleset.
    """
    def __init__(self, game):
        self.game = game

    def start(self, players):
        sig.soulbounds(players)
        sig.cont()

    def set_lives(self):
        """How many lives each player should have."""
        return 3

    def player_death(self, p):
        """Handle player death."""
        self.player_reduce_lives(p, 1)
        return self.player_reduce_lives(p.get_soulbound(), 1)
    
    def player_reduce_lives(self, p, n):
        if n == 0:
            return
        p.set_lives(p.get_lives() - n)
        if p.get_lives() == 0:
            return True
        if p.get_lives() == 1:
            sig.player_red(p)
            p.set_hostile(True)
        return False

    def player_kill(self, p1):
        """Handle player kills."""
        return self.player_death(p1)
    
    def assign_boogey(self, players):
        return

    def give_life(self, p1, p2):
        return False
    
    def assign_soulmates(self, players):
        assigned = []
        player_copy = players.copy()
        while len(player_copy) > 0:
            p = player_copy[0]
            if p.get_soulbound() != None:
                pass
            assigned.append(p)
            player_copy.remove(p)
            soulbound = choice(players)
            while soulbound.get_soulbound() != None or soulbound == p:
                soulbound = choice(player_copy)
            p.set_soulbound(soulbound)
            soulbound.set_soulbound(p)
            
            player_copy.remove(soulbound)
        return assigned
    
    def can_ally(self, players):
        return True