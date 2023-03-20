import math
import random
import copy
import sys
from NamedTuples import State, ChildrenContent, NodeValue, SlagResultaat
from Search import Search
from GespeeldeKaart import GespeeldeKaart

class MCTS_Node:
    INF = 1.0e308
    
    def __init__(self, state):                   
        self.stateUitpakken(state)   
        
        self.numberOfVisits = 0
        self.children = [] # = [ ChildrenContent=(kaart, node) ...] 
        self.hand = self.handenDict[self.huidigeSpeler]
        self.searchMachine = Search()
        
    # -----------------------------------------------------------------------

    def calc_UCB1(self):
        if self.isRoot():
            return 0
        
        if self.numberOfVisits == 0:
            return self.INF
    
        parentVisits = self.parent.getNumberOfVisits()
        if parentVisits == 0:
            return self.INF

        averageValue = self.aantalPuntenNZ / parentVisits
        part2 = 2 * math.sqrt(math.log(parentVisits / self.numberOfVisits))

        return averageValue + part2
    
    # -----------------------------------------------------------------------
    
        
                                              
    def selectNode(self):
        # OKAY      
        currentNode = self
        while not currentNode.isLeaf():              
            currentNode = currentNode._max_UCB1_Node()
            currentNode = currentNode.node
            
        return currentNode
    # -----------------------------------------------------------------------
    
    def _max_UCB1_Node(self):
         # OKAY
        bestNode = None
        maxValue = -self.INF
        
        if self.isLeaf():
            print("Onverwachte leaf ", self.actions)
            sys.exit(1)
        
        for child in self.children:
            tmp = child.node.calc_UCB1()
            if tmp == self.INF:
                return NodeValue(child.node, tmp)
            
            if tmp > maxValue:
                maxValue = tmp
                bestNode = child.node

        if bestNode == None:
            print("Onverwacht geen Node gevonden")
            sys.exit(1)
        
        return NodeValue(bestNode, maxValue)
    
    # -----------------------------------------------------------------------

    def expand(self):
        print("expand uitvoeren ")
        for card in  self.searchMachine.speelbareKaarten(self.hand, \
                                                  self.gevraagdeKleur, \
                                                  self.troef):
            """            
            print("kaarten in huidige slag: ")
            for c in self.kaartenHuidigeSlag:
                print(c.card, end = ", ")
            print()
            """

            # voor iedere kaart moet een nieuwe state en node worden aangemaakt
            # aanpassen: handenDict, kaartenHuidigeSlag, huidigeSpeler, aantalPuntenNZ
            
            nwActions = copy.deepcopy(self.actions)
            nwActions.append(card)
            
            nwHandenDict = copy.deepcopy(self.handenDict)
            nwHandenDict[self.huidigeSpeler].removeCard(card)
            
            nwKaartenHuidigeSlag = copy.deepcopy(self.kaartenHuidigeSlag)
            nwKaartenHuidigeSlag.append(GespeeldeKaart(self.huidigeSpeler, card))

            
            if len(self.kaartenHuidigeSlag) == 0: # eersteKaart
                   # kaarten die in de huidige slag gespeeld zijn
                nwGevraagdeKleur = card.kleur
                self.gevraagdeKleur = card.kleur
            else:
                nwGevraagdeKleur = self.gevraagdeKleur
  
            toenamePunten = 0     
            if  len(self.kaartenHuidigeSlag) == 4: # vierdekaart:
                # "toenamePunten winnaar") # winnaar is windrichting
                slagResultaat = \
                    self.searchMachine.toenameSlagen(self.troef, self.kaartenHuidigeSlag)
                nwHuidigeSpeler = slagResultaat.winnaar
                toenameGerealiseerdeSlagen = slagResultaat.toenamePunten 
                for k in self.kaartenHuidigeSlag:
                    print(str(k), end = ', ')
                print("winnaar = ", slagResultaat.winnaar, "winst/verlies = ", toenameGerealiseerdeSlagen, " totaal = ", (self.aantalPuntenNZ + toenamePunten))
            else:
                nwHuidigeSpeler = self.searchMachine.volgendeSpeler[self.huidigeSpeler]
                
            state = State(self, nwHandenDict, nwHuidigeSpeler, nwActions, \
                                self.troef,nwKaartenHuidigeSlag,  \
                                self.aantalPuntenNZ + toenamePunten)
            
            node = MCTS_Node(state)
            
            self.children.append(ChildrenContent(card, node)) 
            print("expand card =  ", card)
        print("Einde expand")
            
    # -----------------------------------------------------------------------
        
    def rollOut(self):
        copyHanden = copy.deepcopy(self.handenDict)
        speler = self.huidigeSpeler
          
        kaarten = self.searchMachine.speelbareKaarten(copyHanden[speler], \
                                    self.gevraagdeKleur, self.troef)
        
        if (len(kaarten) == 0):
            return 
        
        print("rollOut speelbareKaarten:", end = ' ')
        for k in kaarten:
            print(k, end = ', ')
        print("")
        
        #selecteer een random action
        index = random.randint(0, len(kaarten) - 1)
        kaart = kaarten[index]
        
        copyHanden[speler].removeCard(kaart)
        
        tmp = random.randint(-3, 4)
        tmp = 0
        print("rollOut geselecteerd: ", str(kaart), " geschatte waarde ", tmp)
        
        speler = self.searchMachine.volgendeSpeler[speler]
        """ 
            -eerste kaart  --> kleur/troef
            -laatste kaart --> update aantalpunten
                volgendespeler = winaar
              anders volgendespeler = nexPlayer(huidigeSpeler)
            -verwijder randomKaart
        """
        
        #return self.aantalBehaaldeSlaagen
        
        print("rollOut moet nog recursief verder zoeken")
        return tmp
    
    # -----------------------------------------------------------------------

    def backPropagate(self, value):
        # OKAY 
        self.aantalPuntenNZ += value
        self.numberOfVisits += 1

        if not self.isRoot():
            self.parent.backPropagate(value)      
     
    # -----------------------------------------------------------------------    

    def getNumberOfVisits(self):
        # OKAY
        return self.numberOfVisits
    
    # -----------------------------------------------------------------------
    
    def getBestchildAndValue(self): # (node, value)
        bestCouple = None 
        
        for child in self.children:
            if bestCouple == None:
               bestCouple = NodeValue(child.node, child.node.calc_UCB1()) 
            else:
                tmp = child.node.calc_UCB1()
                if tmp > bestCouple.value :
                    bestCouple = NodeValue(child.node, tmp)
                    
        return bestCouple
    
    # -----------------------------------------------------------------------
    
    def showResult(self):
        bestCouple = self.getBestchildAndValue()
        
        if bestCouple != None:
            print("actie = ", bestCouple.action, " value = ", bestTrio.value)
        
            if bestTrio.node != None:
                bestTrio.node.showNextAction()

    # -----------------------------------------------------------------------
    
    def stateUitpakken(self, state) :
        self.parent = state.parent                  
        self.handenDict = state.handenDict
        self.huidigeSpeler = state.huidigeSpeler
        self.actions = state.actions
            # laatste kaart heeft tot deze node heeft geleid.
        self.troef = state.troef
        self.kaartenHuidigeSlag = state.kaartenHuidigeSlag
        self.aantalKaartenInSlag = len(self.kaartenHuidigeSlag)
        
        if self.aantalKaartenInSlag == 0:
            self.gevraagdeKleur = None
        else:
            self.gevraagdeKleur = self.kaartenHuidigeSlag[0].card.kleur
    
        self.aantalPuntenNZ = state.aantalPuntenNZ
        
    # -----------------------------------------------------------------------
    
    def getFirstChildNode(self):
        return self.children[0]
    
     # -----------------------------------------------------------------------
    
    def toonAlles(self, index=1):
        print("Node DFS-index: ", index)
        print(self) 
        for x in self.children:
            #print("op niveau ", index, x.kaart, x.node.huidigeSpeler)
            #print(self)
            x.node.toonAlles(index + 1)
        print()
    
    # -----------------------------------------------------------------------

    def isRoot(self) :
        # OKAY
        return self.parent == None
    
    # -----------------------------------------------------------------------

    def isLeaf(self):
        # OKAY
        return len(self.children ) == 0

    # -----------------------------------------------------------------------
    
    def __str__(self):
        tmp = f"MCTS_Node: actions = "
        for k in self.actions:
            tmp += str(k) + ", "
            
        
        tmp += f"speler = {self.huidigeSpeler}, aantal children: {len(self.children)}, aantalPuntenNZ = {self.aantalPuntenNZ}, numberOfVisits = {self.numberOfVisits }"
        
        return tmp
