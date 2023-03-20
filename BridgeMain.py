import cProfile
import io
import pstats
from pstats import SortKey

import Constantes
from Deck import Deck
from Search import Search, MAX_VALUE


def maakSpelersKaarten(handen):
    result = {}

    for hand in handen:
        result[hand.windrichting] = hand.getKaartenLijst()

    return result


spel = Deck()
#hand = spel.geefRandomVierHanden()
#hand.toonKaarten()

#print("\n ---------------------- \n\n")
aantalSlagen = 9
handen = spel.geefRandomVierHanden(aantalSlagen)
for hand in handen:
    hand.toonKaarten()

spelersKaarten = maakSpelersKaarten(handen)

zoekmachine = Search()

gespeeldeKaarten = []

print("start zoeken")

pr = cProfile.Profile()
pr.enable()

besteWaarde, gespeeldeKaarten = \
    zoekmachine.alphaBetaSearch(aantalSlagen, Constantes.OOST, 1, None, None,
                                0, spelersKaarten, gespeeldeKaarten,
                               -MAX_VALUE, MAX_VALUE)

pr.disable()

print("klaar:")
print(zoekmachine.teller)
print(zoekmachine.tel)

s = io.StringIO()
sortby = SortKey.CUMULATIVE
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())


print("Best gespeelde kaarten: ")
print(f"besteWaarde = {besteWaarde}")
regelteller = 0
for spelerKaart in gespeeldeKaarten:
    print(str(spelerKaart))
    regelteller += 1
    if regelteller == 4:
        print()
        regelteller = 0
