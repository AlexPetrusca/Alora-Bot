from enum import Enum


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


class Prayer(Enum):
    PROTECT_FROM_MELEE = 1610, 960
