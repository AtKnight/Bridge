import Constantes

class Suit:
    def __init__(self, suit):
        if suit in Constantes.ALL_SUITS:
            self.suit = suit
            self.cards = []

    def add_Card(self, card):
        self.cards.append(card)

    def __str__(self):
        result = f'{self.suit}'
        first = True

        for c in self.cards:
            if first:
                result.append(f' {c}')
                first = False
            else:
                result.append(f', {c}')

