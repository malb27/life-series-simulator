from random import randint, choice, shuffle

import gameMessages.fillerEarly as fillEarly
import gameMessages.filler as filler
import gameMessages.playerDeath as playerDeath
import gameMessages.playerKill as playerKill
import gameMessages.minorPositive as minPos
import gameMessages.minorNegative as minNeg
import gameMessages.majorPositive as majPos
import gameMessages.majorNegative as majNeg

from playerclass import Player

# Create subclasses later on, as requirements change
class Signaller():
    def eventHandler(self, players, s1, s2, source, tag):
        if len(players) == 1:
            print(tag + choice(source.ONE_PERSON).format(p = players[0].getName()))
        else:
            if players and (not s2 or randint(0, len(players)) < 3):
                print(tag*len(players) + choice(source.ONE_GROUP).format(g = Player.getNameString(players)))
            else:
                s = 's' if len(s1) == 1 else ''
                print(tag + choice(source.TWO_GROUP).format(g1 = Player.getNameString(s1), g2 = Player.getNameString(s2), s = s))
    

    def allianceCreate(self, members, name):
        print("[+] {players} have made an alliance! ({n})".format(players = members, n = name))

    def allianceDisband(self):
        pass

    def allianceLeave(self):
        pass

    def allianceKick(self):
        pass

    def eventMajorPos(self, s1, s2):
        self.eventHandler([], s1, s2, majPos, '')

    def eventMajorNeg(self, s1, s2):
        self.eventHandler([], s1, s2, majNeg, '')

    def eventMinorPos(self, s1, s2):
        self.eventHandler([], s1, s2, minPos, '')

    def eventMinorNeg(self, s1, s2):
        self.eventHandler([], s1, s2, minNeg, '')

    def gameEnd(self):
        pass

    def playerDeath(self, players):
        self.eventHandler(players, players, [], playerDeath, '[-] ')

    def playerEliminated(self, player):
        print("[X] {p} has been eliminated!".format(p = player))

    def playerEscape(self, player, attackers):
        s = 's' if len(attackers) > 1 else ''
        print(choice(playerKill.ESCAPES).format(p = player.getName(), s = s, s2 = 's'.replace(s,''), a = choice(attackers).getName()))

    def playerFight(self, s1, s2):
        print("A fight breaks out between {players}!".format(players = Player.getNameString(s1 + s2)))

    def playerKilled(self, p, a):
        print("[-]", choice(playerKill.KILLS).format(p1 = p.getName(), p2 = a.getName()))

    def filler(self, players, s1, s2, sesh):
        if sesh < 3:
            self.eventHandler(players, s1, s2, fillEarly, '')
            return
        self.eventHandler(players, s1, s2, filler, '')
    
    def stats(self, players, eliminated):
        print("")
        players.sort(key=lambda p: p.getLives(), reverse=True)
        for p in players:
            print("{name} ({ally}): {lives}".format(name = p.getName(), ally = p.getAllianceName(), lives = p.getLives()))

        # print("")
        # players.sort(key=lambda p: p.getLives(), reverse=True)
        # all = players + eliminated
        # for p in all:
        #     elim = '[ELIMINATED]' if p.getLives() == 0 else ''
        #     print("{name} ({ally}): {lives} {elim}".format(name = p.getName(), ally = p.getAllianceName(), lives = p.getLives(), elim = elim))

    def statsEnd(self, players, eliminated):
        print("\n[ [ Game End: Winner is {player} ] ]".format(player = players[0].getName()))
        print("\nFINAL STANDINGS")
        all = players + eliminated
        for i, p in enumerate(all, start=1):
            s = '' if p.getKills() == 1 else 's'
            print("#{i}: {name} ({k} kill{s})".format(i = i, name = p.getName(), k = p.getKills(), s = s))