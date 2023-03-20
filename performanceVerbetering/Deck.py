import Constantes
import random

from Kaart import Kaart
from Hand import Hand


class Deck:
    def __init__(self):
        self._kaarten = [Kaart(kleur, waarde) for kleur in Constantes.ALLE_KLEUREN
                         for waarde in Constantes.ALLE_KAARTWAARDEN]

    def schudden(self):
        result = []
        getallen = list(range(0, 52))

        random.seed(1)

        for i in range(0, 52):
            index = random.choice(getallen)
            result.append(self._kaarten[index])
            getallen.remove(index)

        self._kaarten = result


    def geefVierHanden(self, aantal=13):
        handen = []
        handen.append(Hand(Constantes.NOORD, self._kaarten[0: aantal]))
        handen.append(Hand(Constantes.OOST, self._kaarten[aantal: 2 * aantal]))
        handen.append(Hand(Constantes.ZUID, self._kaarten[2 * aantal: 3 * aantal]))
        handen.append(Hand(Constantes.WEST, self._kaarten[3 * aantal: 4 * aantal]))

        return handen


    def geefRandomVierHanden(self, aantal=13):
        self.schudden()
        return self.geefVierHanden(aantal)


    def __len__(self):
        return len(self._kaarten)


    def __getitem__(self, positie):
        return self._kaarten[positie]
