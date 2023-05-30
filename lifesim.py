"""
Main simulator functionality.
"""

from random import randint, choice, choices, shuffle
from math import ceil, floor

from gameMap import Map
from playerManagement import Player, Alliance, REL_CAP
from rulesets import ThirdLife
from signallers import sig

HOURS = 3

class Game():
    """The actual simulator."""
    def __init__(self):
        self.rule = None
        self.all = []
        self.players = []
        self.eliminated = []
        self.alliances = []
        self.map = None
        self.relationships = []
        self.session = 0

    def init(self):
        """Setup to start the game."""
        self.map = Map(ceil(len(self.players)/2))
        self.relationships = [None] * len(self.players)
        for i in range(len(self.players)):
            self.relationships[i] = [0] * len(self.players)

    def add_player(self, name): # Add support for stats later
        """Adds a new player to the roster."""
        player = Player(len(self.players), name, self.rule.set_lives())
        self.players.append(player)
        self.all.append(player)

    def set_rules(self, ruleset):
        """Sets the ruleset the game users."""
        self.rule = ruleset

    def get_relationship(self, play_1, play_2):
        """Gets the relationship between two players."""
        # Add boogey penalty later
        rel = (self.relationships[play_1.get_index()][play_2.get_index()]
                + Alliance.get_alliance_bonus(play_1,play_2))

        # Actual relation value can go over -5/5, but returned value is hard capped
        return min(REL_CAP, rel) if rel > 0 else max(-REL_CAP, rel)

    # Randomly decay relationships - move values closer to 0
    def decay_relationships(self):
        """Randomly decays relationships over the course of the game."""
        for i, player in enumerate(self.relationships):
            for j in range(0, len(player)):
                val = self.relationships[i][j]
                self.relationships[i][j] -= (int(val/abs(val))
                                             if val != 0 and randint(0,1) == 0 else 0)

    def player_elimination(self, player):
        """Eliminates a player from the game."""
        sig.player_eliminated(player)
        self.players.remove(player)
        self.eliminated.insert(0, player)
        alliance = player.get_alliance()
        if player.leave_alliance(self.relationships): # Alliance has disbanded
            self.alliances.remove(alliance)

    def generate_conflict_sides(self, attacker, defender, participants):
        """Sorts players into either side of a conflict using relationship values.
        Players can be spectators if not sorted."""

        participants.remove(attacker)
        participants.remove(defender)

        if len(participants) == 0: # Only 2 players in combat, no need to assign sides
            self.relationships[attacker.get_index()][defender.get_index()] -= randint(3,4)
            sig.player_fight([attacker], [defender])
            return [attacker], [defender]

        attackers = [attacker]
        defenders = [defender]

        for player in participants:
            a_rel = self.get_relationship(player, attacker)
            d_rel = self.get_relationship(player, defender)
            if d_rel == REL_CAP or randint(0,REL_CAP-d_rel) == 0:
                defenders.append(player)
            elif player.is_hostile() and (a_rel == REL_CAP or randint(0, REL_CAP-a_rel) == 0):
                attackers.append(player)

        for defender in defenders:
            for attacker in attackers:
                self.relationships[defender.get_index()][attacker.get_index()] -= randint(3,4)

        sig.player_fight(attackers, defenders)
        return attackers, defenders

    def battle(self, attack, defence):
        """Battles two sides against each other."""

        a_sum = 0
        d_sum = 0

        for attacker in attack:
            a_sum += randint(0,10) + (3 if attacker.get_lives() == 1 else 0)
        for defender in defence:
            d_sum += randint(0,10) + (3 if defender.get_lives() == 1 else 0)
        winning, losing = (defence, attack) if a_sum < d_sum else (attack, defence)

        for player in losing:
            if randint(0, len(winning)) == 0:
                sig.player_escape(player, winning)
            else:
                attacker = choice(winning)
                sig.player_killed(player, attacker)
                self.relationships[player.get_index()][attacker.get_index()] -= (randint(1,3)
                    + (floor(REL_CAP/3) if player.get_alliance() is not None
                       and player.get_alliance() == attacker.get_alliance()
                    else 0))
                if self.rule.player_death(player):
                    self.player_elimination(player)
                attacker.inc_kills()

    def generate_conflict(self, participants, hostiles):
        """Checks if conflict occurs between any players."""

        # For each hostile, force conflict if relationship is at min value or few surviving players
        # Otherwise, generate number based on relationship - lives - modifier affected by survivors
        # If any land on 0 or less, conflict - otherwise return False
        for hostile in hostiles:
            for target in participants:
                val = (0 if self.get_relationship(hostile, target) == -REL_CAP
                       or len(self.players) < 4 # Force conflict if very few players remain
                       else randint(0, REL_CAP+self.get_relationship(hostile, target))
                       - target.get_lives()
                       - floor((2*REL_CAP)/len(self.players)))
                if val <= 0 and hostile.get_index() != target.get_index():
                    side1, side2 = self.generate_conflict_sides(hostile, target, participants)
                    self.battle(side1, side2)
                    return True
        return False

    def generate_single_player_event(self, player):
        """Creates an event for a single player."""
        if (player.get_alliance() is None):
                max_val = max(self.relationships[player.get_index()])
                indices = [i for i, val in enumerate(self.relationships[player.get_index()])
                                if val == max_val]
                shuffle(indices)
                if (max_val > -ceil(REL_CAP/2) 
                        and (max_val >= ceil(REL_CAP/2) 
                             or randint(0,ceil(REL_CAP/2)-max_val)) - floor(10/self.session) <= 0):
                    for index in indices:
                        alliance = self.all[index].get_alliance()
                        if (alliance and len(alliance.get_members()) < ceil(len(self.players)/3)):
                            sig.alliance_join(player, alliance.get_name())
                            player.set_alliance(alliance)
                            return

        match randint(1,20):
            case filler if player.get_lives() <= filler <= 1:
                sig.player_death([player])
                if self.rule.player_death(player):
                    self.player_elimination(player)
            case _:
                if (player.is_hostile() and randint(0,1) == 0):
                    sig.player_trap(self.map.set_trap(player), player, [], False)
                    return
                if (len(self.eliminated) > 0 and randint(0,REL_CAP) == 0):
                    sig.event_deadloot([player], choice(self.eliminated))
                    return
                sig.filler([player], [], [], self.session)

    def generate_event(self, participants, sector):
        """Generates an event for the playeres in a sector."""

        # Updates relationships between two groups
        def relation_update(side1, side2, sign, amount):
            for play1 in side2:
                for play2 in side1:
                    index1, index2 = play1.get_index(), play2.get_index()
                    self.relationships[index1][index2] += sign*randint(amount[0],amount[1])
                    if sign > 0:
                        self.relationships[index2][index1] += randint(amount[0],amount[1])

        # Handler for alliance related events
        def alliance_event(participants, type_of_inter):
            alliance = choice(self.alliances)
            sig.event_alliance(participants, alliance.get_name(), type_of_inter)
            return alliance.get_members()

        # If trap in sector, trigger it
        if sector.get_trap() and len(self.players) > len(participants):
            tripped = bool(sector.get_trap_setter() in participants and randint(0,10) == 0)
            if sector.get_trap_setter() not in participants or tripped:
                kill, text, setter = sector.trigger_trap(len(participants), tripped)
                sig.player_trap(text, setter, participants, kill)
                if kill:
                    found = choice([True, False])
                    for player in participants:
                        if found:
                            self.relationships[player.get_index()][setter.get_index()] -= (3
                                + (floor(REL_CAP/3) if player.get_alliance() is not None
                                   and player.get_alliance() == setter.get_alliance()
                                else 0))
                        if self.rule.player_death(player):
                            self.player_elimination(player)
                        if setter != player:
                            setter.inc_kills()
                return

        # Alliance event
        if len(participants) < 4 and len(self.alliances) > 0 and randint(0, HOURS*6) == 0:
            match randint(1,6):
                case pos if pos in [1,2]:
                    alliance_event(participants, 'ip')
                case neg if neg in [3,4]:
                    alliance_event(participants, 'in')
                case 5:
                    alliance_event(participants, 'mp')
                case 6:
                    alliance_event(participants, 'mn')
            return

        # If only player in sector
        if len(participants) == 1:
            self.generate_single_player_event(participants[0])
            return

        # Create a new alliance.
        # Ensures an alliance between ALL surviving players cannot be made.
        if (len(self.players) > len(participants) and randint(0,HOURS-1) == 0
                and all(p.get_alliance() is None for p in participants)):
            name = sig.alliance_create(participants)
            if name is not None:
                ally = Alliance(name)
                for player in participants:
                    player.set_alliance(ally)
                self.alliances.append(ally)
                return

        # Push event generation to rulesets potentially in future?
        # Lots of repeated code even with template structure, tweaking will be difficult
        side1, side2 = self.generate_sides(participants)
        match randint(1,15):
            case filler if 1 <= filler <= 5:
                if (len(self.eliminated) > 0 and randint(0,REL_CAP) == 0):
                    sig.event_deadloot(participants, choice(self.eliminated))
                    return
                sig.filler(participants, side1, side2, self.session)
            case pos if pos in [6,7]:
                sig.event(side1, side2, 'ip')
                relation_update(side1, side2, 1, [1,2])
            case neg if neg in [8,9]:
                sig.event(side1, side2, 'in')
                relation_update(side1, side2, -1, [1,2])
            case 10:
                sig.event(side1, side2, 'mp')
                relation_update(side1, side2, 1, [2,4])
            case 11:
                sig.event(side1, side2, 'mn')
                relation_update(side1, side2, -1, [2,4])
            case death if 12 <= death <= 15:
                sig.player_death(side1)
                for player in side1:
                    if self.rule.player_death(player):
                        self.player_elimination(player)

    def run_day(self):
        """Run a single day/session of the game."""
        self.session += 1
        self.map.update_sectors(ceil(len(self.players)/2))
        sig.game_next_sesh(self.session)
        for _ in range(0, HOURS):
            if self.run_hour(self.map.allocate_sector(self.players)):
                sig.stats_win(self.players[0])
                sig.cont()
                sig.stats_end(self.players, self.eliminated)
                return True

        # Relationship Decay
        if self.session % 3:
            self.decay_relationships()

        sig.cont()
        sig.stats(self.players, self.alliances, self.session)
        sig.cont()
        return False

    def run_hour(self, sectors):
        """Run a single hour of the game."""
        for sector in sectors:
            hostile = sector.get_hostile()
            participants = sector.get_players()
            if len(participants) == 0: # No players in sector
                continue
            if len(hostile) == 0 or not self.generate_conflict(participants, hostile):
                self.generate_event(participants, sector)

            # There should always be 1 player left, but the check is present
            # incase something somehow goes wrong
            if len(self.players) < 2:
                return True

        # Check alliance stability
        for alliance in self.alliances:
            if alliance.disband(self.relationships):
                self.alliances.remove(alliance)

        return False

    @staticmethod
    def generate_sides(participants):
        """Split a group of players into two sides."""
        player_set = set(participants)
        side1 = set(choices(participants, k=randint(1, len(participants)-1)))
        side2 = list(player_set - side1)
        side1 = list(side1)
        return side1, side2

    # def start(self):
    #     print("\n-- STARTING LIVES --")
    #     for p in self.players:
    #         print("{name}: {n} lives".format(name = p.get_name(), n = p.get_lives()))


if __name__ == "__main__":
    game = Game()
    rule = ThirdLife(game)
    game.set_rules(rule)
    sig.start()
    players = input("\nPlayers: ").split(", ") # Sanitise if frontend ever made

    for p in players:
        game.add_player(p)
    game.init()

    # game.start()

    while not game.run_day():
        continue
