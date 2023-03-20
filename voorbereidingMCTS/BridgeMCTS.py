from NamedTuples import State
from Kaart import Kaart

import Constantes

from Deck import Deck
from MCTS import MCTS

if  __name__ == "__main__":        
    deck = Deck()
    deck.leesHanden()
    deck.toon()

    # kaartenHuidigeSlag = [gespeeldeKaarten, ...]
    state = State(None, deck.handenDict, Constantes.NOORD, [Kaart()], None, [], 0)
    #   namedtuple("State", "parent handenDict huidigeSpeler actions troef kaartenHuidigeSlag aantalPuntenNZ")
    
    mcts = MCTS(state)
    print("deck bevat ", deck.getNumberOfCards(), " aantal kaarten")
    #mcts.search(deck.getNumberOfCards())
    mcts.search(100000)
    #mcts.showResult()
    mcts.toonAlles()

    