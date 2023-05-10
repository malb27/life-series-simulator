from random import randint, choice, shuffle

from functools import reduce

import gameMessages.fillerEarly as fillEarly
import gameMessages.filler as filler
import gameMessages.playerDeath as playerDeath
import gameMessages.playerKill as playerKill
import gameMessages.minorPositive as minPos
import gameMessages.minorNegative as minNeg
import gameMessages.majorPositive as majPos
import gameMessages.majorNegative as majNeg

from os import system

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

    DEATH = '\033[91m'
    ALLIANCE = '\033[96m'
    DISBAND = '\033[36m'
    INFO = '\033[93m'

# Create subclasses later on, as requirements change
class CmdSigaller():
    def eventHandler(self, players, s1, s2, source, tag):
        if len(players) == 1:
            print(tag + choice(source.ONE_PERSON)
                  .format(p = CmdSigaller.getNameString(players)))
        else:
            if players and (not s2 or randint(0, len(players)) < 3):
                print(tag*len(players) + choice(source.ONE_GROUP)
                      .format(g = CmdSigaller.getNameString(players)))
            else:
                s = 's' if len(s1) == 1 else ''
                print(tag + choice(source.TWO_GROUP)
                      .format(g1 = CmdSigaller.getNameString(s1),
                              g2 = CmdSigaller.getNameString(s2),
                              s = s))
    

    def start(self):
        print(CmdSigaller.colour("Welcome to the Life Simulator!", bc.PURPLE))
        print("Enter a list of players separated by commas and spaces. Press ENTER to start the simulator.")
        print("e.g. Player1, Player2, Player3")

    def allianceCreate(self, members, name):
        print(CmdSigaller.colour("[+] {players} have made an alliance! {n}", bc.ALLIANCE)
              .format(players = CmdSigaller.getNameString(members),
                      n = CmdSigaller.colour('(' + name + ')', bc.ALLIANCE)))

    def allianceDisband(self, a):
        print(CmdSigaller.colour("[?] {alliance} has fallen apart...".format(alliance = a), bc.DISBAND))

    def allianceJoin(self, p, a):
        print(CmdSigaller.colour("[+] {p} has joined {ally}!", bc.ALLIANCE)
              .format(p = CmdSigaller.getNameString([p]), ally = CmdSigaller.colour(a, bc.ALLIANCE)))

    def allianceLeave(self, p, a):
        print("{p} has left {ally}."
              .format(p = CmdSigaller.getNameString([p]), ally = CmdSigaller.colour(a, bc.ALLIANCE)))

    def allianceKick(self, p, a):
        print("{p} was kicked from {ally}."
              .format(p = CmdSigaller.getNameString([p]), ally = CmdSigaller.colour(a, bc.ALLIANCE)))

    def eventMajorPos(self, s1, s2):
        self.eventHandler([], s1, s2, majPos, '')

    def eventMajorNeg(self, s1, s2):
        self.eventHandler([], s1, s2, majNeg, '')

    def eventMinorPos(self, s1, s2):
        self.eventHandler([], s1, s2, minPos, '')

    def eventMinorNeg(self, s1, s2):
        self.eventHandler([], s1, s2, minNeg, '')

    def filler(self, players, s1, s2, sesh):
        if sesh < 3:
            self.eventHandler(players, s1, s2, fillEarly, '')
            return
        self.eventHandler(players, s1, s2, filler, '')

    def gameNextSesh(self, i):
        print(CmdSigaller.colour("\n. : Session {num} : .".format(num = i), bc.INFO))

    def playerDeath(self, players):
        self.eventHandler(players, players, [], playerDeath, CmdSigaller.colour('[-] ', bc.DEATH))

    def playerEliminated(self, player):
        print(CmdSigaller.colour("[X] {p} has been eliminated!", bc.DEATH).format(p = player.getName()))

    def playerEscape(self, player, attackers):
        s = 's' if len(attackers) > 1 else ''
        print(choice(playerKill.ESCAPES)
              .format(p = CmdSigaller.getNameString([player]),
                      s = s,
                      s2 = 's'.replace(s,''),
                      a = CmdSigaller.getNameString([choice(attackers)])))

    def playerFight(self, s1, s2):
        print("A fight breaks out between {players}!"
              .format(players = CmdSigaller.getNameString(s1 + s2)))

    def playerKilled(self, p, a):
        print(CmdSigaller.colour("[-]", bc.DEATH), choice(playerKill.KILLS)
              .format(p1 = CmdSigaller.getNameString([p]),
                      p2 = CmdSigaller.getNameString([a])))
        
    def playerRed(self, player):
        print(CmdSigaller.colour("[!] {player} is now red!", bc.RED)
              .format(player = CmdSigaller.getNameString([player])))
    
    def stats(self, players, i):
        print("\nSESSION {num} STANDINGS:".format(num = i))
        players.sort(key=lambda p: p.getLives(), reverse=True)
        for p in players:
            print("{name} ({ally}): {lives}"
                  .format(name = CmdSigaller.getNameString([p]),
                          ally = p.getAllianceName(),
                          lives = p.getLives()))

    def statsEnd(self, players, eliminated):
        print("\n-- FINAL STANDINGS --")
        all = players + eliminated
        for i, p in enumerate(all, start=1):
            s = '' if p.getKills() == 1 else 's'
            print(f"#{i}: {p.getName()} {CmdSigaller.colour(f'({p.getKills()} kill{s})', bc.GREY)}")
        input(CmdSigaller.colour("\n[ Press Enter to Exit ]", bc.GREY))

    def statsWin(self, player):
        print("\n[ [ Game End: Winner is {player} ] ]"
              .format(player = CmdSigaller.colour(player.getName(), bc.PURPLE)))
        
    def cont(self):
        input(CmdSigaller.colour("\n[ Press ENTER to Continue ]", bc.GREY))

    @staticmethod
    def getNameString(players):
        if len(players) == 1:
            return CmdSigaller.getNameColour(players[0])
        def combine(x, y):
            return x + ", " + y
        pStr = map(lambda x: CmdSigaller.getNameColour(x), players[:-1])
        return reduce(combine, pStr) + " and " + CmdSigaller.getNameColour(players[-1])
    
    @staticmethod
    def getNameColour(player):
        playStr = player.getName() + bc.ENDC
        lives = player.getLives()
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
        return col + playStr
    
    @staticmethod
    def colour(string, colour):
        return colour + string + bc.ENDC

sig = CmdSigaller()