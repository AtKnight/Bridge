from Hands import Hands

class Game:
    def __init__(self):
        self.event = ""     # string
        self.site = ""      # string
        self.date = ""      # string YYYY.MM.DD
        self.board = -1 
        self.west = ""      # string player
        self.north = ""     # string player
        self.east = ""      # string player
        self.south = ""     # string player
        self.dealer = ""    # string
        self.vulnerable = ""
        self.deal = {}      # dictionary S --> Cards ... C --> Cards
        self.scoring = ""   # string scoring method
        self.declarer = ""  # string
        self.contract = ""  # string
        self.result = -1
        self.hands = Hands()
        
    def set_event(self, event):
        self.event = event
        
    def set_site(self, site):
        self.site = site
        
    def set_date(self, date):
        self.date = date

    def set_board(self, board):
        self.board = board

    def set_west(self, west):
        self.west = west

    def set_north(self, north):
        self.north = north
        
    def set_east(self, east):
        self.east = east

    def set_south(self, south):
        self.south = south
        
    def set_dealer(self, dealer):
        self.dealer = dealer
        
    def set_vunerable(self, vunerable):
        self.vunerable = vunerable
        
    def set_deal(self, deal):
        self.deal = deal

    def set_scoring(self, scoring):
        self.scoring = scoring
        
    def set_declarer(self, declarer):
        self.declarer = declarer

    def set_contract(self, contract):
        self.contract = contract
        
    def set_result(self, result):
        self.result = result

