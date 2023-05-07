from random import randint, choice

import gameMessages.fillerEarly as fillEarly
import gameMessages.filler as filler
import gameMessages.playerDeath as playerDeath

from playerclass import Player

# Create subclasses later on, as requirements change
class Signaller():
    def eventHandler(self, players, s1, s2, source, tag):
        if len(players) == 1:
            print(tag + choice(source.ONE_PERSON).format(p = players[0].getName()))
        else:
            if not s2 or randint(0, len(players)) < 3:
                print(tag*len(players) + choice(source.ONE_GROUP).format(g = Player.getNameString(players)))
            else:
                s = 's' if len(s1) == 1 else ''
                print(tag + choice(source.TWO_GROUP).format(g1 = Player.getNameString(s1), g2 = Player.getNameString(s2), s = s))
    

    def allianceCreate(self, members, name):
        print("[+] {players} have made an alliance! ({n})".format(players = members, n = name))

    def allianceDisband(self):
        pass

    def gameEnd(self):
        pass

    def playerAttack(self):
        pass

    def playerDeath(self, players):
        self.eventHandler(players, players, [], playerDeath, '[-] ')

    def playerDefend(self):
        # test for allyship
        pass

    def playerEliminated(self, player):
        print("[X] {p} has been eliminated!".format(p = player))

    def playerEscape(self):
        pass

    def playerJoin(self):
        pass

    def playerKilled(self):
        pass

    def filler(self, players, s1, s2, sesh):
        if sesh < 3:
            # self.fillerEarly(players, s1, s2)
            self.eventHandler(players, s1, s2, fillEarly, '')
            return
        self.eventHandler(players, s1, s2, filler, '')

        # if len(players) == 1:
        #     print(choice(filler.ONE_PERSON_FILLERS).format(p = players[0].getName()))
        # else:
        #     if randint(0, len(players)) < 2:
        #         print(choice(filler.ONE_GROUP_FILLERS).format(g = Player.getNameString(players)))
        #     else:
        #         print(s1, s2)
        #         s = 's' if len(s1) == 1 else ''
        #         print(choice(filler.TWO_GROUP_FILLERS).format(g1 = Player.getNameString(s1), g2 = Player.getNameString(s2), s = s))


    # def fillerEarly(self, players, s1, s2):
    #     # if len(players) == 1:
    #     #     print(choice(fillEarly.ONE_PERSON_FILLERS).format(p = players[0].getName()))
    #     # else:
    #     #     if randint(0, len(players)) < 2:
    #     #         print(choice(fillEarly.ONE_GROUP_FILLERS).format(g = Player.getNameString(players)))
    #     #     else:
    #     #         print(s1, s2)
    #     #         s = 's' if len(s1) == 1 else ''
    #     #         print(choice(fillEarly.TWO_GROUP_FILLERS).format(g1 = Player.getNameString(s1), g2 = Player.getNameString(s2), s = s))

    #     self.eventHandler(players, s1, s2, fillEarly)

    