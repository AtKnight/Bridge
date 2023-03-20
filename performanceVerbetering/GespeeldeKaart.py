
class GespeeldeKaart:
    def __init__(self, speler, card):
        self.speler = speler
        self.card = card

    def __str__(self):
        return f"{self.speler:5} speelt {str(self.card):}"

    def print(self):
        print(self.speler)
        print(self.card)
