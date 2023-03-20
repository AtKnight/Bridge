import Constantes


class Hand:
    def __init__(self, windrichting, kaartLijst):

        self.windrichting = windrichting
        self.troef = None
        self._ordenKaarten(kaartLijst)
        self.regelmatigeVerdeling = self.heeftRegelmatigeVerdeling()
        self.aantalHonneursPunten = self.aantalPlaatjesPunte()
        self.maxLengteKleur = self.maxKleurLengte()

    def _ordenKaarten(self, kaartLijst):
        self.klaverenKaarten = []
        self.ruitenKaarten = []
        self.hartenKaarten = []
        self.schoppenKaarten = []

        for kaart in self.sortKaarten(kaartLijst):
            if kaart.kleur == Constantes.SCHOPPEN:
                self.schoppenKaarten.append(kaart)
            elif kaart.kleur == Constantes.HARTEN:
                self.hartenKaarten.append(kaart)
            elif kaart.kleur == Constantes.RUITEN:
                self.ruitenKaarten.append(kaart)
            elif kaart.kleur == Constantes.KLAVEREN:
                self.klaverenKaarten.append(kaart)

    def sortKaarten(self, kaartLijst):
        # kaarten is een list van Kaart.
        # Sorteert op schoppen, harten, ruiten en klaver.
        # Binnen een kleur wordt gesorteerd op A, K, V, B, 10 .. 2

        return sorted(kaartLijst, reverse=True, key=lambda x: x.key)

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

    def toonKaarten(self):
        print(f'windrichting:                {self.windrichting}')
        self._toonKleurKaart(Constantes.SCHOPPEN, self.schoppenKaarten)
        self._toonKleurKaart(Constantes.HARTEN, self.hartenKaarten)
        self._toonKleurKaart(Constantes.RUITEN, self.ruitenKaarten)
        self._toonKleurKaart(Constantes.KLAVEREN, self.klaverenKaarten)
        print(f'regelmatige verdeling:       {self.regelmatigeVerdeling}\n' +
              f'aantal punten voor honneurs: {self.aantalHonneursPunten}\n' +
              f'max kleur en lengte:         {self.maxLengteKleur}\n')

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

