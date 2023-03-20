import cProfile
import io
import pstats
from pstats import SortKey

import Constantes
from Deck import Deck
from Search import Search, MAX_VALUE

# ---------------------------------------------------------

def main(aantalSlagen):
    
    deck = Deck(aantalSlagen)
    deck.toon()
 
    handenDict = deck.getHanden()
    
    zoekmachine = Search()

    gespeeldeKaartenLijst = []

    print("start zoeken")

    # ++  --> PERFORMANCE METING
    pr = cProfile.Profile()
    pr.enable()
    
    besteWaarde, gespeeldeKaartenLijst = \
        zoekmachine.alphaBetaSearch(aantalSlagen, Constantes.OOST, 1, None, None,
                                    0, handenDict, gespeeldeKaartenLijst,
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
    
    # ++ <-- PERFORMANCE METING
    
    print("Best gespeelde kaarten: ")
    print(f"besteWaarde = {besteWaarde}")
    
    regelteller = 0
    for spelerKaart in gespeeldeKaartenLijst:
        print(str(spelerKaart))
        regelteller += 1
        if regelteller == 4:
            print()
            regelteller = 0



# ---------------------------------------------------------


if  __name__ == "__main__":
    aantalSlagen = 6
    main(aantalSlagen)

    
