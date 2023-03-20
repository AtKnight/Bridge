import Constants

from Hand import Hand

class Hands:
    def __init__(self):
        self.hands = {}
        print("Hands Hand nog vullen")
        self.hands[ND] = Hand()

    def addHand(self, hand):
        self.hands.append(hand)

    def addCard(self, direction, card):
        #  direction is N, E, S, W
        #  card is an object of Card
        self.hands[direction].addCard(card)