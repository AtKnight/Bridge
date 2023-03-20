from collections import namedtuple

State           = namedtuple("State", "parent handenDict huidigeSpeler actions troef kaartenHuidigeSlag aantalPuntenNZ")
ChildrenContent = namedtuple("ChildrenContent", "kaart node")
NodeValue       = namedtuple("ActionNodeValue", "node value")
SlagResultaat   = namedtuple("SlagResultaat", "toenamePunten winnaar") # winnaar is windrichting