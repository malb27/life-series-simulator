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

# Create subclasses later on, as requirements change
class Signaller():
    def eventHandler(self, players, s1, s2, source, tag):
        if len(players) == 1:
            print(tag + choice(source.ONE_PERSON)
                  .format(p = players[0].getName()))
        else:
            if players and (not s2 or randint(0, len(players)) < 3):
                print(tag*len(players) + choice(source.ONE_GROUP)
                      .format(g = Signaller.getNameString(players)))
            else:
                s = 's' if len(s1) == 1 else ''
                print(tag + choice(source.TWO_GROUP)
                      .format(g1 = Signaller.getNameString(s1),
                              g2 = Signaller.getNameString(s2),
                              s = s))
    

    def allianceCreate(self, members, name):
        print("[+] {players} have made an alliance! ({n})"
              .format(players = Signaller.getNameString(members),
                      n = name))

    def allianceDisband(self, a):
        print("[?] {alliance} has fallen apart...".format(alliance = a))

    def allianceLeave(self, p, a):
        print("{p} has left {ally}.".format(p = p, ally = a))

    def allianceKick(self, p, a):
        print("{p} was kicked from {ally}.".format(p = p, ally = a))

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
        print("\n. : Session {num} : .".format(num = i))

    def playerDeath(self, players):
        self.eventHandler(players, players, [], playerDeath, '[-] ')

    def playerEliminated(self, player):
        print("[X] {p} has been eliminated!".format(p = player))

    def playerEscape(self, player, attackers):
        s = 's' if len(attackers) > 1 else ''
        print(choice(playerKill.ESCAPES)
              .format(p = player.getName(),
                      s = s,
                      s2 = 's'.replace(s,''),
                      a = choice(attackers).getName()))

    def playerFight(self, s1, s2):
        print("A fight breaks out between {players}!"
              .format(players = Signaller.getNameString(s1 + s2)))

    def playerKilled(self, p, a):
        print("[-]", choice(playerKill.KILLS)
              .format(p1 = p.getName(),
                      p2 = a.getName()))
        
    def playerRed(self, player):
        print("[!] {player} is now red!".format(player = player))
    
    def stats(self, players, i):
        print("\nSESSION {num} STANDINGS:".format(num = i))
        players.sort(key=lambda p: p.getLives(), reverse=True)
        for p in players:
            print("{name} ({ally}): {lives}"
                  .format(name = p.getName(),
                          ally = p.getAllianceName(),
                          lives = p.getLives()))

    def statsEnd(self, players, eliminated):
        print("\n[ [ Game End: Winner is {player} ] ]"
              .format(player = players[0].getName()))
        print("\n-- FINAL STANDINGS --")
        all = players + eliminated
        for i, p in enumerate(all, start=1):
            s = '' if p.getKills() == 1 else 's'
            print("#{i}: {name} ({k} kill{s})"
                  .format(i = i,
                          name = p.getName(),
                          k = p.getKills(),
                          s = s))

    @staticmethod
    def getNameString(players):
        if len(players) == 1:
            return players[0].getName()
        def combine(x, y):
            return x + ", " + y
        pStr = map(lambda x: x.getName(), players[:-1])
        return reduce(combine, pStr) + " and " + players[-1].getName()

sig = Signaller()