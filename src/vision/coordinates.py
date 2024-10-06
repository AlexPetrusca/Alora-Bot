from enum import Enum

from src.vision.regions import Regions


# todo: coordinates should be specified in scaled XY (0.0-1.0, 0.0-1.0)
def rescale_coord(x, y):
    if (Regions.SCREEN.w, Regions.SCREEN.h) == (1728, 1117):
        return x, y
    else:
        M2_TOP_OFFSET = 37
        ratio_x = Regions.GAME.w / (1728 - Regions.RUNELITE_SIDEBAR.w)
        ratio_y = Regions.GAME.h / (1117 - M2_TOP_OFFSET)
        return round(ratio_x * x), round(ratio_y * (y - M2_TOP_OFFSET))


class Player(Enum):
    POSITION = rescale_coord(855, 585)


class ControlPanel(Enum):
    COMBAT_TAB = Regions.CONTROL_PANEL.offset(24, 18)
    STATS_TAB = Regions.CONTROL_PANEL.offset(57, 18)
    QUEST_TAB = Regions.CONTROL_PANEL.offset(90, 18)
    INVENTORY_TAB = Regions.CONTROL_PANEL.offset(123, 18)
    EQUIPMENT_TAB = Regions.CONTROL_PANEL.offset(156, 18)
    PRAYER_TAB = Regions.CONTROL_PANEL.offset(189, 18)
    MAGIC_TAB = Regions.CONTROL_PANEL.offset(222, 18)

    CLAN_TAB = Regions.CONTROL_PANEL.offset(24, 316)
    FRIEND_TAB = Regions.CONTROL_PANEL.offset(57, 316)
    IGNORE_TAB = Regions.CONTROL_PANEL.offset(90, 316)
    LOGOUT_TAB = Regions.CONTROL_PANEL.offset(123, 316)
    OPTIONS_TAB = Regions.CONTROL_PANEL.offset(156, 316)
    EMOTE_TAB = Regions.CONTROL_PANEL.offset(189, 316)
    MUSIC_TAB = Regions.CONTROL_PANEL.offset(222, 316)

    BANK_CLOSE = Regions.BANK.offset(470, 17)


class Minimap(Enum):
    COMPASS = Regions.MINIMAP.offset(54, 20)
    HEALTH = Regions.MINIMAP.offset(39, 58)
    PRAYER = Regions.MINIMAP.offset(39, 93)
    RUN = Regions.MINIMAP.offset(50, 126)
    SPECIAL = Regions.MINIMAP.offset(73, 151)


# dx = 26, dy = 24
class StandardSpellbook(Enum):
    HOME_TELEPORT = Regions.CONTROL_PANEL.offset(45, 48)


# dx = 40, dy = 27
class ArceuusSpellbook(Enum):
    HOME_TELEPORT = Regions.CONTROL_PANEL.offset(45, 48)
    RESURRECT_GREATER_GHOST = Regions.CONTROL_PANEL.offset(84, 212)
    RESURRECT_GREATER_SKELETON = Regions.CONTROL_PANEL.offset(124, 212)
    RESURRECT_GREATER_ZOMBIE = Regions.CONTROL_PANEL.offset(164, 212)


# dx = 37, dy = 37
class Prayer(Enum):
    PROTECT_FROM_MAGIC = Regions.CONTROL_PANEL.offset(82, 174)
    PROTECT_FROM_MISSILES = Regions.CONTROL_PANEL.offset(119, 174)
    PROTECT_FROM_MELEE = Regions.CONTROL_PANEL.offset(156, 174)
    EAGLE_EYE = Regions.CONTROL_PANEL.offset(193, 174)
    MYSTIC_MIGHT = Regions.CONTROL_PANEL.offset(45, 211)
    PIETY = Regions.CONTROL_PANEL.offset(82, 248)


class BarrowsCoord(Enum):
    SPADE = Regions.CONTROL_PANEL.offset(53, 52)  # todo: replace usages with Inventory.ITEM_1_1
    REWARDS_CLOSE = Regions.REWARD.offset(218, 18)


class CerberusCoord(Enum):
    WALK1 = rescale_coord(850, 50)
    WALK2 = rescale_coord(750, 90)
    WALK3 = rescale_coord(850, 215)


class HealCoord(Enum):
    WALK1 = rescale_coord(700, 302)
    PRAYER_ALTAR = rescale_coord(1292, 68)
    HEALER = rescale_coord(805, 520)
    BANK_CHEST = rescale_coord(1080, 524)


class TeleportCoord(Enum):
    TELEPORT_WIZARD = rescale_coord(695, 255)

    SEARCH_BUTTON = Regions.TP_MENU.offset(24, 17)
    SEARCH_FIRST_RESULT = Regions.TP_MENU.offset(217, 52)
    SEARCH_SECOND_RESULT = Regions.TP_MENU.offset(217, 82)
