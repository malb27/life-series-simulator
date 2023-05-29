"""
Handles event broadcasting.
"""

from random import randint, choice
from functools import reduce
from os import system

import gameMessages.fillerEarly as fillEarly
import gameMessages.filler as filler
import gameMessages.playerDeath as playerDeath
import gameMessages.playerKill as playerKill
import gameMessages.minorPositive as minPos
import gameMessages.minorNegative as minNeg
import gameMessages.majorPositive as majPos
import gameMessages.majorNegative as majNeg

import gameMessages.allianceName as allyName
import gameMessages.allianceInteract as allyInt

import gameMessages.standardMessages as standMsg

system('color')

class bc:
    ENDC = '\033[0m'

    RED = '\033[31m'
    YELLOW = '\033[33m'
    GREEN = '\033[92m'
    DARKGREEN = '\033[32m'
    PURPLE = '\033[95m'
    DARKPURPLE = '\033[35m'
    GREY = '\033[90m'
    BLUE = '\033[34m'

    DEATH = '\033[91m'
    ALLIANCE = '\033[96m'
    DISBAND = '\033[36m'
    INFO = '\033[93m'

# Create subclasses later on, as requirements change
class CmdSigaller():
    """Handles command-line output messages to signal events."""
    def event_handler(self, players, side1, side2, source, tag):
        """Standard handler for events, regardless of number of players."""
        if len(players) == 1:
            print(tag + choice(source.ONE_PERSON)
                  .format(p = CmdSigaller.get_name_string(players)))
        else:
            if players and (not side2 or randint(0, len(players)) < 3):
                print(tag*len(players) + choice(source.ONE_GROUP)
                      .format(g = CmdSigaller.get_name_string(players)))
            else:
                plural = 's' if len(side1) == 1 else ''
                print(tag + choice(source.TWO_GROUP)
                      .format(g1 = CmdSigaller.get_name_string(side1),
                              g2 = CmdSigaller.get_name_string(side2),
                              s = plural))

    def start(self):
        """Prints the startup message."""
        print(CmdSigaller.colour(standMsg.WELCOME, bc.PURPLE))
        print(standMsg.INSTRUCTIONS)

    def alliance_create(self, members):
        """Prints the alliance creation message."""
        first, second = choice(allyName.FIRST), choice(allyName.SECOND)
        allyName.FIRST.remove(first)
        allyName.SECOND.remove(second)
        name = first + " " + second

        print(CmdSigaller.colour(standMsg.ALLIANCE, bc.ALLIANCE)
              .format(players = CmdSigaller.get_name_string(members),
                      n = CmdSigaller.colour(f'({name})', bc.ALLIANCE)))

        return name

    def alliance_disband(self, alliance):
        """Prints the alliance disband message."""
        print(CmdSigaller.colour(standMsg.ALLIANCE_DISBAND
                                 .format(alliance = alliance), bc.DISBAND))

    def alliance_join(self, player, alliance):
        """Prints a new player joining an alliance."""
        print(CmdSigaller.colour(standMsg.ALLIANCE_JOIN, bc.ALLIANCE)
              .format(p = CmdSigaller.get_name_string([player]),
                      alliance = CmdSigaller.colour(alliance, bc.ALLIANCE)))

    def alliance_leave(self, player, alliance):
        """Prints a player leaving an alliance."""
        print(standMsg.ALLIANCE_LEAVE
              .format(p = CmdSigaller.get_name_string([player]),
                      alliance = CmdSigaller.colour(alliance, bc.ALLIANCE)))

    def alliance_kick(self, player, alliance):
        """Prints a player being kicked from an alliance."""
        print(standMsg.ALLIANCE_KICK
              .format(p = CmdSigaller.get_name_string([player]),
                      alliance = CmdSigaller.colour(alliance, bc.ALLIANCE)))

    def event(self, side1, side2, type_of_event):
        """Prints the event text."""
        event_set = None
        match type_of_event:
            case "mp":
                event_set = majPos
            case "mn":
                event_set = majNeg
            case "ip":
                event_set = minPos
            case "in":
                event_set = minNeg
        self.event_handler([], side1, side2, event_set, '')

    def event_alliance(self, group, alliance, type_of_event):
        """Print the alliance event text."""
        event_set = None
        match type_of_event:
            case "mp":
                event_set = allyInt.MAJPOS
            case "mn":
                event_set = allyInt.MAJNEG
            case "ip":
                event_set = allyInt.MINPOS
            case "in":
                event_set = allyInt.MINNEG

        plural1 = 's' if len(group) == 1 else ''
        plural2 = '' if alliance[-1] == 's' else 's'
        print(choice(event_set)
              .format(g = CmdSigaller.get_name_string(group),
                      ally = CmdSigaller.colour(alliance, bc.ALLIANCE),
                      s = plural1,
                      s2 = plural2))

    def event_deadloot(self, player, dead):
        """Prints message for looting dead players."""
        plural = 's' if len(player) == 1 else ''
        print(standMsg.DEADLOOT
              .format(p = CmdSigaller.get_name_string(player),
                      d = CmdSigaller.get_name_string([dead]),
                      s = plural))

    def filler(self, players, side1, side2, sesh):
        """Prints filler text."""
        if sesh < 3:
            self.event_handler(players, side1, side2, fillEarly, '')
            return
        self.event_handler(players, side1, side2, filler, '')

    def game_next_sesh(self, i):
        """Prints banner for a new session."""
        print(CmdSigaller.colour(standMsg.SESSION_HEADER.format(num = i), bc.INFO))

    def player_death(self, players):
        """Prints player death message."""
        self.event_handler(players, players, [], playerDeath, CmdSigaller.colour('[-] ', bc.DEATH))

    def player_eliminated(self, player):
        """Prints player eliminated message."""
        print(CmdSigaller.colour(standMsg.ELIMINATION, bc.DEATH)
              .format(p = player.get_name()))

    def player_escape(self, player, attackers):
        """Prints player escaping from combat message."""
        plural = 's' if len(attackers) > 1 else ''
        print(choice(playerKill.ESCAPES)
              .format(p = CmdSigaller.get_name_string([player]),
                      s = plural,
                      s2 = 's'.replace(plural,''),
                      a = CmdSigaller.get_name_string([choice(attackers)])))

    def player_fight(self, side1, side2):
        """Prints player fight message."""
        print(standMsg.FIGHT
              .format(players = CmdSigaller.get_name_string(side1 + side2)))

    def player_killed(self, player, attacker):
        """Prints player killed message."""
        print(CmdSigaller.colour("[-]", bc.DEATH), choice(playerKill.KILLS)
              .format(p1 = CmdSigaller.get_name_string([player]),
                      p2 = CmdSigaller.get_name_string([attacker])))

    def player_red(self, player):
        """Prints player red message."""
        print(CmdSigaller.colour(standMsg.RED, bc.RED)
              .format(p = CmdSigaller.get_name_string([player])))

    def player_trap(self, template, player, target, kill):
        """Prints messages associated with traps being set off."""
        plural, plural2 = ('s', "was") if len(target) == 1 else ('', "were")
        col = bc.DEATH if kill else bc.BLUE
        print(CmdSigaller.colour(template, col)
              .format(p = CmdSigaller.get_name_string([player]),
                      w = plural2,
                      s = plural,
                      p2 = CmdSigaller.get_name_string(target)))

    def stats(self, players, alliances, i):
        """Print end of day stats."""
        def print_player(player):
            print("{name}: {lives}"
                .format(name = CmdSigaller.get_name_string([player]),
                    lives = player.get_lives()))

        print(standMsg.STANDINGS.format(num = i))
        player_set = set(players)

        first = True # need a more elegant way to do this
        for alliance in alliances:
            if not first:
                print()
            first = False
            print(CmdSigaller.colour(alliance.get_name(), bc.ALLIANCE))
            alliance.get_members().sort(key=lambda p: p.get_lives(), reverse=True)
            for member in alliance.get_members():
                print_player(member)
            player_set -= set(alliance.get_members())

        if len(player_set) > 0:
            if len(player_set) < len(players):
                print(CmdSigaller.colour("\nNo Alliance", bc.ALLIANCE))
            player_set = list(player_set)
            player_set.sort(key=lambda p: p.get_lives(), reverse=True)
            for player in player_set:
                print_player(player)

    def stats_end(self, players, eliminated):
        """Prints end of game stats."""
        print(standMsg.FINAL_STANDINGS)
        all_players = players + eliminated
        for i, player in enumerate(all_players, start=1):
            plural = '' if player.get_kills() == 1 else 's'
            print(standMsg.RANK
                  .format(num = i,
                          p = player.get_name(),
                          kills = CmdSigaller.colour(f'({player.get_kills()} kill{plural})', bc.GREY)))
        input(CmdSigaller.colour(standMsg.EXIT, bc.GREY))

    def stats_win(self, player):
        """Prints winner banner."""
        print(standMsg.WINNER
              .format(p = CmdSigaller.colour(player.get_name(), bc.PURPLE)))

    def cont(self):
        """Prints continuing message."""
        input(CmdSigaller.colour(standMsg.CONTINUE, bc.GREY))

    @staticmethod
    def get_name_string(players):
        """Gets a list of names from a list of players."""
        if len(players) == 0:
            return ''
        if len(players) == 1:
            return CmdSigaller.get_name_colour(players[0])
        def combine(x, y):
            return x + ", " + y
        player_string = map(lambda x: CmdSigaller.get_name_colour(x), players[:-1])
        return reduce(combine, player_string) + " and " + CmdSigaller.get_name_colour(players[-1])

    @staticmethod
    def get_name_colour(player):
        """Gets the colour associated with a player's life count."""
        player_string = player.get_name() + bc.ENDC
        lives = player.get_lives()
        col = ''
        match lives:
            case 0:
                col = bc.GREY
            case 1:
                col = bc.RED
            case 2:
                col = bc.YELLOW
            case 3:
                col = bc.GREEN
            case _:
                col = bc.DARKGREEN
        return col + player_string

    @staticmethod
    def colour(string, colour):
        """Adds colour codes to a string."""
        return colour + string + bc.ENDC

sig = CmdSigaller()
