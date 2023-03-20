import Constantes
import General
import Suit
import Card

from Suit import Suit


class Hand:
    def __init__(self):
        self.suit_cards = {}

        for suit in Constantes.ALL_SUITS:
            self.suit_cards[suit] = Suit(suit)

        self.troef = None
        self._ordenKaarten(kaartLijst)
        self.regelmatigeVerdeling = self.heeftRegelmatigeVerdeling()
        self.aantalHonneursPunten = self.aantalPlaatjesPunten()
        self.maxLengteKleur = self.maxKleurLengte()


    def sortKaarten(self):
        # Wordt gesorteerd op A, K, V, B, 10 .. 2

        def cardValue(card):
            if card.value == Constantes.AH:
                return 14
            if card.value == Constantes.KH:
                return 13
            if card.value == Constantes.QH:
                return 12
            if card.value == Constantes.JH:
                return 11

            return int(card.value)

        return sorted(kaartLijst, reverse=True, key = cardValue(card))

    # -----------------------------------------------------------------------

    def heeftRegelmatigeVerdeling(self):
        # Wordt gebruikt om te bepalen of 1 SA geboden kan worden
        tmp = [len(self.klaverenKaarten), len(self.ruitenKaarten),
               len(self.hartenKaarten), len(self.schoppenKaarten)]
        tmp.sort()

        return tmp in [[3, 3, 3, 4], [2, 3, 4, 4], [2, 3, 3, 5]]

    def aantalPlaatjesPunte(self):
        result = 0
        for kaart in self.klaverenKaarten + self.ruitenKaarten + \
                     self.hartenKaarten + self.schoppenKaarten:
            result += kaart.biedWaarde

        return result

    def maxKleurLengte(self):
        # De volgorde van de if-statement zorgt er voor dat bij gelijke lengtes
        # de juiste volgorde wordt bepaald.

        result = (Constantes.SCHOPPEN, len(self.schoppenKaarten))
        if len(self.hartenKaarten) > result[1]:
            result = (Constantes.HARTEN, len(self.hartenKaarten))
        if len(self.klaverenKaarten) > result[1]:
            result = (Constantes.KLAVEREN, len(self.klaverenKaarten))
        if len(self.ruitenKaarten) > result[1]:
            result = (Constantes.RUITEN, len(self.ruitenKaarten))

        return result

    # -----------------------------------------------------------------------

    def setTroef(self, kleur):
        self.troef = kleur

    def getStr(self): # returns for every suit the cards as string
                      # all strings have the same length
                      # result is a dictonary suit --> cards
        length = []
        result = {}
        index = 0
        for s in Constantes.SHORT_SUITES:
            result[s]= str(self.suit_cards[s])
            length [index] = len(result[2])
            index += 1

        maxLength = max(length)

        index = 0
        for s in Constantes.SHORT_SUITES:
            result[s] += (maxLength - length[index]) * " "

        return result

        """"
        print(f'regelmatige verdeling:       {self.regelmatigeVerdeling}\n' +
              f'aantal punten voor honneurs: {self.aantalHonneursPunten}\n' +
              f'max kleur en lengte:         {self.maxLengteKleur}\n')
        """

    def _toonKleurKaart(self, kleur, kaartenLijst):
        print(f'{kleur:10}', end=' ')

        for k in kaartenLijst:
            print(f'{k.waarde:>2}', end=' ')
        print()

    def getKaartenLijst(self):
        # Wordt gebruikt door Search alfabeta algoritme
        result = {}
        result[Constantes.SCHOPPEN] = self.schoppenKaarten
        result[Constantes.HARTEN] = self.hartenKaarten
        result[Constantes.RUITEN] = self.ruitenKaarten
        result[Constantes.KLAVEREN] = self.klaverenKaarten

        return result

