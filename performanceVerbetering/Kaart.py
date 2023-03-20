import Constantes

class Kaart:
    def __init__(self, kleur, waarde):
        self.kleur = kleur
        self.waarde = waarde # A K V B 10 9 .. 2
        self.key = self._getKey()
        self.biedWaarde = self._bepaalBiedWaarde()


    def _bepaalBiedWaarde(self):
        if self.waarde.isdigit():
            return 0
        else:
            honneurs = Constantes.HONNEURS
            waardes = {honneurs[0]: 1, honneurs[1]: 2, honneurs[2]: 3, honneurs[3]: 4}

            return waardes[self.waarde]


    def hogerDan(self, kaart, troef):
        if self.kleur == kaart.kleur:
            return self.key > kaart.key
        else:
            return troef != None and kaart.kleur != troef


    def _getKey(self):
        # retourneert conversie[kleur] +  '02', '03' ..'10', 'B' .. 'A'
        # Wordt gebruikt om kaarten te sorteren klaver-2 .. schoppen-A
        # en om de hoogte van de kaarten te vergelijken.

        conversie = {Constantes.SCHOPPEN: '3', Constantes.HARTEN: '2',
                     Constantes.RUITEN: '1', Constantes.KLAVEREN: '0',
                     Constantes.HONNEURS[0]: '11', Constantes.HONNEURS[1]: '12',
                     Constantes.HONNEURS[2]: '13', Constantes.HONNEURS[3]: '14'}

        tmp = str(self.waarde)
        if tmp.isdigit():
            w = '0' + tmp if len(tmp) == 1 else tmp
        else:
            w =conversie[tmp]

        # w = '02', '03' ..'10', 'B' .. 'A'

        k = conversie[self.kleur]

        return k + w


    def __eq__(self, other):
        return self.kleur == other.kleur and self.waarde == other.waarde


    def __str__(self):
        return self.kleur + ' ' + str(self.waarde)

