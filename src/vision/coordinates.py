from enum import Enum


class Player(Enum):
    POSITION = 855, 585


class Interface(Enum):
    MAGIC_TAB = 1674, 801
    PRAYER_TAB = 1641, 801
    EQUIPMENT_TAB = 1608, 801
    INVENTORY_TAB = 1575, 801
    QUEST_TAB = 1541, 801
    STATS_TAB = 1508, 801
    COMBAT_TAB = 1475, 801
    BANK_CLOSE = 1074, 110


class Minimap(Enum):
    COMPASS = 1535, 57
    HEALTH = 1522, 95
    PRAYER = 1522, 130
    RUN = 1534, 162
    SPECIAL = 1555, 187


class StandardSpellbook(Enum):
    HOME_TELEPORT = 1496, 832


class ArceuusSpellbook(Enum):
    HOME_TELEPORT = 1496, 832
    RESURRECT_GREATER_SKELETON = 1575, 996


# x: 1496 - 1644  -->  5 columns  -->  37 gap
# y:  845 - 1030  -->  6 rows     -->  37 gap
class Prayer(Enum):
    PROTECT_FROM_MAGIC = 1533, 956
    PROTECT_FROM_MISSILES = 1570, 956
    PROTECT_FROM_MELEE = 1607, 956
    EAGLE_EYE = 1644, 956
    MYSTIC_MIGHT = 1496, 993
    PIETY = 1533, 1030


class BarrowsCoords(Enum):
    SPADE = 1512, 845
    REWARDS_CLOSE = 922, 417


class CerberusCoords(Enum):
    WALK1 = 850, 50
    WALK2 = 750, 90
    WALK3 = 850, 215


class HealCoords(Enum):
    WALK1 = 700, 302
    PRAYER_ALTAR = 1292, 68
    HEALER = 805, 520
    BANK_CHEST = 1080, 524


class TeleportCoords(Enum):
    TELEPORT_WIZARD = 695, 255
    SEARCH_BUTTON = 608, 363
    SEARCH_FIRST_RESULT = 800, 400
