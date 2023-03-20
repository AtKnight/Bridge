import Constantes

from Deck import Deck
from Search import Search, MAX_VALUE

import cProfile, pstats, io
from pstats import SortKey

def maakSpelersKaarten(handen):
    result = {}

    for hand in handen:
        result[hand.windrichting] = hand.getKaartenLijst()

    return result


spel = Deck()
hand = spel.geefRandomVierHanden()[0]
hand.toonKaarten()

print("\n ---------------------- \n\n")
aantalRondes = 3
handen = spel.geefRandomVierHanden(aantalRondes)
for hand in handen:
    hand.toonKaarten()


spelersKaarten = maakSpelersKaarten(handen)


zoekmachine = Search()


gespeeldeKaarten = []

print("start zoeken")

pr = cProfile.Profile()
pr.enable()

besteWaarde, gespeeldeKaarten = zoekmachine.alphaBetaSearch(aantalRondes, Constantes.OOST, 1, None, None,
                                                            0, spelersKaarten, gespeeldeKaarten,
                                                            -MAX_VALUE, MAX_VALUE)

pr.disable()

print("klaar:")

s = io.StringIO()
sortby = SortKey.CUMULATIVE
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
#print(s.getvalue())


print("Best gespeelde kaarten: ")
print(f"besteWaarde = {besteWaarde}")
regelteller = 0
for spelerKaart in gespeeldeKaarten:
    print(str(spelerKaart))
    regelteller += 1
    if regelteller == 4:
        print()
        regelteller = 0

