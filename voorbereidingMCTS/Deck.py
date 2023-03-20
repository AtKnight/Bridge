import random
import Constantes

from Kaart import Kaart
from Hand import Hand


class Deck:
    def __init__(self, aantalKaartenPerHand = 0):
        if aantalKaartenPerHand == 0:
            self._kaarten = []
            self.handenDict = {}
        else:
            self._kaarten = [Kaart(kleur, waarde)
                         for kleur in Constantes.ALLE_KLEUREN
                         for waarde in Constantes.ALLE_KAARTWAARDEN]
            # [Kaart(SCHOPPEN, 2), Kaart(SCHOPPEN, 3) .. Kaart(KLAVER, 'A')]
        
            self.handenDict = self._maakHanden(aantalKaartenPerHand)
            # {NOORD:[kaarten], OOST:[Kaarten] ...}
       
    # -----------------------------------------------------------------------    

    def schudden(self):
        result = []
        getallen = list(range(0, 52))

        random.seed(1)

        for i in range(0, 52):
            index = random.choice(getallen)
            result.append(self._kaarten[index])
            getallen.remove(index)

        self._kaarten = result

    # -----------------------------------------------------------------------

    def _maakHanden(self, aantalKaartenPerHand):
        # Retourneert vier handen met random aantal Kaarten.
        self.schudden()  
        
        self.handenDict = {}
        
        self.handenDict[Constantes.NOORD] = Hand(Constantes.NOORD, self._kaarten[0: aantalKaartenPerHand])
        self.handenDict[Constantes.OOST]  = Hand(Constantes.OOST,  self._kaarten[aantalKaartenPerHand:     2 * aantalKaartenPerHand])
        self.handenDict[Constantes.ZUID]  = Hand(Constantes.ZUID,  self._kaarten[2 * aantalKaartenPerHand: 3 * aantalKaartenPerHand])
        self.handenDict[Constantes.WEST]  = Hand(Constantes.WEST,  self._kaarten[3 * aantalKaartenPerHand: 4 * aantalKaartenPerHand])
        
        return self.handenDict

    # -----------------------------------------------------------------------
    
    def toon(self):
        for windrichting in Constantes.ALLE_WINDRICHTINGEN:
            self.handenDict[windrichting].toon()
            
    # -----------------------------------------------------------------------
    
    def getHanden(self):
        return self.handenDict
            
    # -----------------------------------------------------------------------
    
    def leesHanden(self):
        print("leesHanden doet niets")
        self.__init__(aantalKaartenPerHand = 5)
        
    # -----------------------------------------------------------------------
    
    def getNumberOfCards(self):
        som = 0
        kaarten = self.handenDict[Constantes.NOORD].kaartenDict
        
        for kleur in Constantes.ALLE_KLEUREN:
            som += len(kaarten[kleur])
            
        return 4 * som

    def __len__(self):
        return len(self._kaarten)

    # -----------------------------------------------------------------------
    
    def __getitem__(self, positie):
        return self._kaarten[positie]
