import re

class Proef:
    WAARDE = ("S", "H", "D", "C")

    def __init__(self):
        print("Proef-object gemaakt")

    def probeer(self):
        print(Proef.WAARDE)

print("start")
#pr = Proef()
#pr.probeer()

str = "N:.63.AKQ987.A9732 A8654.KQ5.T.QJT6 J973.J98742.3.K4 KQT2.AT.J6542.85"
for hand in re.split('\s+', str[2:]):
    print(f'Hand-->{hand}<--')
    suitCards = re.split('\.', hand)
    for sc in suitCards: # cards in (S, H, D, C)
        print(f'suitCards -->{sc}<--')
        if len(sc) > 0:
            for i in range(0, len(sc)): # A, K, Q, J, T ... 2
                m = re.search(sc[i], 'AKQJT98765432')
                if m is None:
                    print("Ongeldig ", sc[i])
        else:
            print("lege string")

    print("")
