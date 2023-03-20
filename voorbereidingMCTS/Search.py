import copy
import Constantes

from Kaart import Kaart
from GespeeldeKaart import GespeeldeKaart
from NamedTuples import SlagResultaat


MAX_VALUE = 10000


class Search:
    def __init__(self):
        self.tel = 0
        self.teller = [0, 0, 0, 0, 0, 0]
        self.dummyKaart = Kaart()
        self.volgendeSpeler = {Constantes.NOORD: Constantes.OOST,
                               Constantes.OOST:  Constantes.ZUID,
                               Constantes.ZUID:  Constantes.WEST,
                               Constantes.WEST:  Constantes.NOORD}
        # Dit sneller dan een function.
        
        self.ALLE_KLEUREN = Constantes.ALLE_KLEUREN

    def alphaBetaSearch(self, diepte, speler, nummerSpeler, gevraagdeKleur,
                        troef, aantalGerealiseerdeSlagen, handenDict,
                        gespeeldeKaarten, alpha, beta):
        # speler= wie ('Noord', ...) moet een kaart neerleggen
        # nummerSpeler =  bijv. 3 is derde speler in deze slag
        # gevraagdeKleur =  none, 'klaver' ..., 'schoppen' zie Constantes
        # troef = zie gevraagde kleur
        # spelersKaarten is {'Noord': [nog te spelen cards], ... 'Zuid': [nog te spelen cards]}
        # gespeeldeKaarten is [(speler, kaart), (speler, kaart) .....]

        if diepte == 0:
            return (aantalGerealiseerdeSlagen, gespeeldeKaarten)

        if self.maximaliseer(speler):
            optimumResult = -MAX_VALUE
            max = optimumResult
        else:
            optimumResult = MAX_VALUE
            min = optimumResult

        besteGespeeldeKaarten = None
        hand = handenDict[speler]

        # bepaal speelbare kaarten
        cards = self.speelbareKaarten(hand, gevraagdeKleur, troef)
        for card in cards:
            self.tel += 1

            if nummerSpeler == 1:
                gevraagdeKleur = card.kleur

            gespeeldeKaarten.append(GespeeldeKaart(speler, card))

            restoreInfo = hand.removeCard(card)

            toenameGerealiseerdeSlagen = 0
            if nummerSpeler == 4:
                # alle speler hebben in deze slag een kaart gespeeld.
                
                # "toenamePunten winnaar") # winnaar is windrichting
                slagResultaat = \
                    self.toenameSlagen(troef, gespeeldeKaarten)
                nextSpeler = slagResultaat.winnaar
                toenameGerealiseerdeSlagen = slagResultaat.toenamePunten 
                
                volgendeNummerSpeler = 1
                gevraagdeKleur = None
                # wordt bepaald aan het begin van de volgende ronde door nextPlayer
                diepteAfname = 1
            else:
                nextSpeler = self.volgendeSpeler[speler]
                volgendeNummerSpeler = nummerSpeler + 1
                diepteAfname = 0

            besteWaarde, nieuweGespeeldeKaarten = self.alphaBetaSearch(
                diepte - diepteAfname, nextSpeler,
                volgendeNummerSpeler, gevraagdeKleur, troef,
                aantalGerealiseerdeSlagen + toenameGerealiseerdeSlagen,
                handenDict, gespeeldeKaarten, alpha, beta)

            hand.restoreCard(card, restoreInfo)
            # plaats de verwijderde kaart weer terug in hand (met speelbare kaarten)

            if self.maximaliseer(speler):
                if besteWaarde >= beta:
                    gespeeldeKaarten.pop()
                    self.teller[nummerSpeler] += 1
                    
                    return besteWaarde, besteGespeeldeKaarten
                    # beta cutoff
                    
                if besteWaarde > max:
                    max = besteWaarde
                    optimumResult = max
                    besteGespeeldeKaarten = copy.copy(nieuweGespeeldeKaarten)

                    if besteWaarde > alpha:
                        alpha = besteWaarde

            else:
                if besteWaarde <= alpha:
                    gespeeldeKaarten.pop()
                    self.teller[nummerSpeler] += 1
                
                    
                    return besteWaarde, besteGespeeldeKaarten
                    # alpha cutoff
                
                if besteWaarde < min:
                    min = besteWaarde
                    optimumResult = min
                    besteGespeeldeKaarten = copy.copy(nieuweGespeeldeKaarten)

                    if besteWaarde < beta:
                        beta = besteWaarde

            gespeeldeKaarten.pop()

        return optimumResult, besteGespeeldeKaarten

    # -----------------------------------------------------------------------

    def speelbareKaarten(self, hand, gevraagdeKleur, troef):
        kaartenDict = hand.getKaartenDict()
         
        if gevraagdeKleur is None:
            # speler die uitkomt bepaalt de kleur.
            # speler kan elk van zijn kaarten spelen.

            result = []
            for kleur in self.ALLE_KLEUREN:
                result.extend(kaartenDict[kleur])

            return result

        if hand.geenKaarten(gevraagdeKleur):
            
            if troef is None or len(hand.kaartenDict[troef]) == 0:
                kaart = self.dummyKaart
                result = [kaart]   
                hand.kaartenDict[kaart.kleur] = result
                # DummyKaart

                return result

            return kaartenDict[troef]

        return kaartenDict[gevraagdeKleur]
    
    # -----------------------------------------------------------------------

    def toenameSlagen(self, troef, gespeeldeKaarten):
        # positieve toename voor slagwinst NZ
        # afname voor slagwinst OW
        
        laatstGespeeldeKaarten = gespeeldeKaarten[-4:]
        laatsteKaart = laatstGespeeldeKaarten[0]
        # voor performance winst
        hoogsteKaart = laatsteKaart.card
        kaartSpeler = winnaar = laatsteKaart.speler

        for i in range(1, 4):
            kaartSpeler = self.volgendeSpeler[kaartSpeler]
            laatsteKaart = laatstGespeeldeKaarten[i].card
            if laatsteKaart.hogerDan(hoogsteKaart, troef):
                hoogsteKaart = laatsteKaart
                winnaar = kaartSpeler

        if winnaar == Constantes.NOORD or winnaar == Constantes.ZUID:
            #toenameGerealiseerdeSlagen = 1
            return SlagResultaat(1, winnaar)
        #else:
            #toenameGerealiseerdeSlagen = -1
        return SlagResultaat(-1, winnaar)
    
        # Dit is een fractie sneller dan het uitgecommentarieerde deel            
        #return toenameGerealiseerdeSlagen, winnaar


    # -------------------------------------------------------------------

    def maximaliseer(self, speler):
        return speler == Constantes.NOORD or speler == Constantes.ZUID
    
     # -------------------------------------------------------------------
     

        