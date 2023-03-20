import Constantes


class Hand:
    def __init__(self, windrichting, kaartLijst):

        self.windrichting = windrichting # NOORD of ... WEST
        self.troef = None                # SCHOPPEN ... KLAVER of None
        self.kaartenDict = {} # {SCHOPPEN: [A, H, .. 2], HARTEN:   }
        self._ordenKaarten(kaartLijst)
        self.regelmatigeVerdeling = self.heeftRegelmatigeVerdeling()
        self.aantalHonneursPunten = self.aantalPlaatjesPunten()
        self.maxLengteKleur = self.maxKleurLengte()

    # -----------------------------------------------------------------------

    def _ordenKaarten(self, kaartLijst):
        for kleur in Constantes.ALLE_KLEUREN:
            self.kaartenDict[kleur] = []
            
        for kaart in self.sortKaarten(kaartLijst):
            self.kaartenDict[kaart.kleur].append(kaart)
            
    # -----------------------------------------------------------------------

    def sortKaarten(self, kaartLijst):
        # Sorteert op schoppen, harten, ruiten en klaver.
        # Binnen een kleur wordt gesorteerd op A, K, V, B, 10 .. 2

        return sorted(kaartLijst, reverse=True, key=lambda x: x.key)

    # -----------------------------------------------------------------------

    def heeftRegelmatigeVerdeling(self):
        # Wordt gebruikt om te bepalen of 1 SA geboden kan worden
        
        tmp = []
        for kleur in Constantes.ALLE_KLEUREN:
            tmp.append(len(self.kaartenDict[kleur]))
            
        tmp.sort()

        return tmp in [[3, 3, 3, 4], [2, 3, 4, 4], [2, 3, 3, 5]]
    
    # -----------------------------------------------------------------------

    def removeCard(self, card):
         lijst = self.kaartenDict[card.kleur]
         index = lijst.index(card)
         del lijst[index]

         return index
     
     # -----------------------------------------------------------------------
     
    def restoreCard(self, card, index):
        self.kaartenDict[card.kleur].insert(index, card)
        
    # -----------------------------------------------------------------------
    
    def geenKaarten(self, kleur):
        return len(self.kaartenDict[kleur]) == 0

    # -----------------------------------------------------------------------

    def aantalPlaatjesPunten(self):
        result = 0
        
        for kleur in Constantes.ALLE_KLEUREN:
            for kaart in self.kaartenDict[kleur]:
                result += kaart.biedWaarde

        return result
    
     # -----------------------------------------------------------------------

    def maxKleurLengte(self):
        # De volgorde van de if-statement zorgt er voor dat bij gelijke lengtes
        # de juiste volgorde wordt bepaald.

        result = (None, -1)
        for kleur in Constantes.ALLE_KLEUREN:
            if len(self.kaartenDict[kleur]) > result[1]:
                result = (kleur, len(self.kaartenDict[kleur]))

        return result

    # -----------------------------------------------------------------------

    def setTroef(self, kleur):
        self.troef = kleur
        
    # -----------------------------------------------------------------------

    def toon(self):
        print(f'windrichting:                {self.windrichting}')
        
        for kleur in Constantes.ALLE_KLEUREN:
            self._toonKleurKaart(kleur, self.kaartenDict[kleur])
            
        print(f'regelmatige verdeling:       {self.regelmatigeVerdeling}\n' +
              f'aantal punten voor honneurs: {self.aantalHonneursPunten}\n' +
              f'max kleur en lengte:         {self.maxLengteKleur}\n')
        
     # -----------------------------------------------------------------------

    def _toonKleurKaart(self, kleur, kaartenLijst):
        print(f'{kleur:10}', end=' ')

        for k in kaartenLijst:
            print(f'{k.waarde:>2}', end=' ')
        print()
        
     # -----------------------------------------------------------------------

    def getKaartenDict(self):
        return self.kaartenDict

    # -----------------------------------------------------------------------
 