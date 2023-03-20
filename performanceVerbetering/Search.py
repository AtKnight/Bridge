import copy
import Constantes

from GespeeldeKaart import GespeeldeKaart

MAX_VALUE = 10000




class Search:
    def __init__(self):
        self.tel = 0
        pass

    def alphaBetaSearch(self, diepte, speler, nummerSpeler, gevraagdeKleur, troef,
                        aantalGerealiseerdeSlagen, spelersKaarten, gespeeldeKaarten, alpha, beta):
        # IS MINIMAX ALGORITME
        # speler= wie ('Noord', ...) moet een kaart neerleggen
        # nummerSpeler =  bijv. 3 is derde speler in deze ronde
        # gevraagdeKleur =  none, 'klaver' ..., 'schoppen' zie Constantes
        # troef = zie gevraagde kleur
        # spelersKaarten is {'Noord': [nog te spelen cards], ... 'Zuid': [nog te spelen cards]}
        # gespeeldeKaarten is [(speler, kaart), (speler, kaart) .....]

        if diepte == 0:
            return (aantalGerealiseerdeSlagen, gespeeldeKaarten)

        if self.maximaliseer(speler):
            optimumResult = -MAX_VALUE
            max = optimumResult
            maximaliseer = True
        else:
            optimumResult = MAX_VALUE
            min = optimumResult
            maximaliseer = False

        besteGespeeldeKaarten = None

        # bepaal speelbare kaarten
        cards = self.speelbareKaarten(spelersKaarten[speler], gevraagdeKleur)
        
        # print(f'Entree diepte = {diepte} speler = {speler}')
        currentDiepte = diepte

        for card in cards:
            if nummerSpeler == 1:
                gevraagdeKleur = card.kleur

            print("diepte = ", diepte, " tel = ", self.tel)

            gespeeldeKaarten.append(GespeeldeKaart(speler, card))

            indexVerwijderdeKaart = self.removeSpelersKaart(card, spelersKaarten[speler])

            toenameGerealiseerdeSlagen = 0
            if self.rondeCompleet(nummerSpeler):
                (toenameGerealiseerdeSlagen, nextSpeler) = self.toenameSlagen(troef, gespeeldeKaarten)
                # nextSpeler is winnaar van de slag
                volgendeNummerSpeler = 1
                gevraagdeKleur = None  # wordt bepaald aan het begin van de volgende ronde door nextPlayer
                diepte -= 1

                self.tel += 1                
            else:
                nextSpeler = self.volgendeSpeler(speler)
                volgendeNummerSpeler = nummerSpeler + 1

            besteWaarde, nieuweGespeeldeKaarten = self.alphaBetaSearch(diepte, nextSpeler,
                                                                                     volgendeNummerSpeler,
                                                                                     gevraagdeKleur, troef,
                                                                                     aantalGerealiseerdeSlagen + toenameGerealiseerdeSlagen,
                                                                                     spelersKaarten,
                                                                                     gespeeldeKaarten, alpha, beta)

            print("Diepte = ", currentDiepte, " waarde uit alfaBeta_1 ", besteWaarde, " tel = ", self.tel)
            if maximaliseer:
                print(" max = ", max)
            else:
                print(" min = ", min)
                
            if nieuweGespeeldeKaarten is None:
                print(nieuweGespeeldeKaarten)
            else:
                index = 1
                for x in nieuweGespeeldeKaarten:
                    print(x)
                    if index == 4:
                        print("++")
                        index = 0
                    index += 1
            print("--------------------")
            

            self.insertSpelersKaart(indexVerwijderdeKaart, card, spelersKaarten[speler])

            if self.maximaliseer(speler):
                if besteWaarde >= beta:
                    gespeeldeKaarten.pop()
                    return besteWaarde, besteGespeeldeKaarten
                    # beta cutoff

                if besteWaarde > max:
                    if besteWaarde == -3 or max == -3:
                        print("Update  max Diepte = ", currentDiepte, " besteWaarde = ", besteWaarde, " max = ", max, " tel = ", self.tel)
                    max = besteWaarde
                    optimumResult = max
                    besteGespeeldeKaarten = copy.deepcopy(nieuweGespeeldeKaarten)

                    if besteWaarde > alpha:
                        alpha = besteWaarde
                        
            else:
                if besteWaarde <= alpha:
                   gespeeldeKaarten.pop()
                   return besteWaarde, besteGespeeldeKaarten
                    # alpha cutoff
                
                if besteWaarde < min:
                    if besteWaarde == -3 or min == -3:
                        print("Update min Diepte = ", currentDiepte, besteWaarde, " min = ", min, " tel = ", self.tel)
                        
                    min = besteWaarde
                    optimumResult = min
                    besteGespeeldeKaarten = copy.deepcopy(nieuweGespeeldeKaarten)

                    if besteWaarde < beta:
                        beta = besteWaarde

            gespeeldeKaarten.pop()

        return optimumResult, besteGespeeldeKaarten

    # --------------------------------------------------------------------------------------------------------

    def speelbareKaarten(self, kaartenDict, gevraagdeKleur):
        result = []

        if gevraagdeKleur == None or len(kaartenDict[gevraagdeKleur]) == 0:
            for kleur in Constantes.ALLE_KLEUREN:
                result.extend(kaartenDict[kleur])

        else:
            result = kaartenDict[gevraagdeKleur]

        return result

    def toenameSlagen(self, troef, gespeeldeKaarten):
        laatstGespeeldeKaarten = gespeeldeKaarten[-4:]
        laatsteKaart = laatstGespeeldeKaarten[0]
        #voor performance winst
        hoogsteKaart = laatsteKaart.card
        kaartSpeler = winnaar = laatsteKaart.speler
        
        for i in range(1, 4):
            kaartSpeler = self.volgendeSpeler(kaartSpeler)
            laatsteKaart = laatstGespeeldeKaarten[i].card
            if laatsteKaart.hogerDan(hoogsteKaart, troef):
                hoogsteKaart = laatsteKaart
                winnaar = kaartSpeler

        if winnaar == Constantes.NOORD or winnaar == Constantes.ZUID:
            toenameGerealiseerdeSlagen = 1
        else:
            toenameGerealiseerdeSlagen = -1

        print("toename = ", toenameGerealiseerdeSlagen)
        return toenameGerealiseerdeSlagen, winnaar


    def removeSpelersKaart(self, card, spelersKaarten):
        lijst = spelersKaarten[card.kleur]
        index = lijst.index(card)
        lijst.pop(index)

        return index
    

    def insertSpelersKaart(self, index, card, spelersKaarten):
        lijst = spelersKaarten[card.kleur].insert(index, card)


    def rondeCompleet(self, playerNumberInTrick):
        return playerNumberInTrick == 4


    def volgendeSpeler(self, player):
        if player == Constantes.NOORD:
            return Constantes.OOST
        
        if player == Constantes.OOST:
           return Constantes.ZUID
        
        if player == Constantes.ZUID:
           return Constantes.WEST
        
        if player == Constantes.WEST:
           return Constantes.NOORD

        print("FOUT IN volgendeSpeler player = ", player)


    def maximaliseer(self, speler):
        return speler == Constantes.NOORD or speler == Constantes.ZUID
