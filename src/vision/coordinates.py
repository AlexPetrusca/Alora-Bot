from enum import Enum

PLAYER_POS = 855, 585
PLAYER_SCREEN_POS = 1710, 1170


class Controls(Enum):
    MAGIC_TAB = 1674, 801
    PRAYER_TAB = 1641, 801
    EQUIPMENT_TAB = 1608, 801
    INVENTORY_TAB = 1575, 801
    QUEST_TAB = 1541, 801
    STATS_TAB = 1508, 801
    COMBAT_TAB = 1475, 801


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
