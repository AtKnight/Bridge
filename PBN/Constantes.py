SPADES = "Spades"
HEARTS = "Hearts"
DIAMONDS = "Diamonds"
CLUBS = "Clubs"

SS = "S"
HS = "H"
DS = "D"
CS = "C"

SHORT_SUITES = (SS, HS, DS, CS) # order is important
ALL_SUITS = (SPADES, HEARTS, DIAMONDS, CLUBS)

NORTH = 'North'
EAST = 'East'
SOUTH = 'South'
WEST = 'West'

ND = "N"
ED = "E"
SD = "S"
WD = "W"

SHORT_DIRECTIONS = (ND, ED, SD, WD)

JH = 'J'
QH = 'Q'
KH = 'K'
AH = 'A'

SHORT_HONORS = (JH, QH, KH, AH)

HONORS_CALL_VALUE = {}
HONORS_CALL_VALUE[JH] = 1
HONORS_CALL_VALUE[QH] = 2
HONORS_CALL_VALUE[KH] = 3
HONORS_CALL_VALUE[AH] = 4

ALL_CARDS_VALUES = [str(n) for n in range(2, 11)] + list(SHORT_HONORS)
