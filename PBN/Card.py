import Constantes
import General

class Card:
    def __init__ (self, suit, value):
        self.suit = suit

        if value in Constantes.ALL_CARDS:
            self.value = value

            if value in Constantes.SHORT_HONORS:
                self.call_value = Constantes.HONORS_CALL_VALUE[value]
        else:
            General.fatal_error(f'Value {value} of card is not correct.')

    def __str__(self):
        return f'{self.suit}{self.value}'
