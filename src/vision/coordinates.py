from enum import Enum

from src.vision.regions import Regions


# todo: coordinates should be specified in scaled XY (0.0-1.0, 0.0-1.0)
def rescale_coord(x, y):
    IS_M2 = (Regions.SCREEN.w, Regions.SCREEN.h) == (1728, 1117)
    if IS_M2:
        return x, y
    else:
        RUNELITE_SIDEBAR_WIDTH = 30
        M2_TOP_OFFSET = 37 if IS_M2 else 0
        ratio_x = Regions.GAME.w / (1728 - RUNELITE_SIDEBAR_WIDTH)
        ratio_y = Regions.GAME.h / (1117 - M2_TOP_OFFSET)
        return round(ratio_x * x), round(ratio_y * (y - M2_TOP_OFFSET))


class Player(Enum):
    POSITION = rescale_coord(855, 585)


class ControlPanel(Enum):
    COMBAT_TAB = Regions.CONTROL_PANEL.x + 24, Regions.CONTROL_PANEL.y + 18
    STATS_TAB = Regions.CONTROL_PANEL.x + 57, Regions.CONTROL_PANEL.y + 18
    QUEST_TAB = Regions.CONTROL_PANEL.x + 90, Regions.CONTROL_PANEL.y + 18
    INVENTORY_TAB = Regions.CONTROL_PANEL.x + 123, Regions.CONTROL_PANEL.y + 18
    EQUIPMENT_TAB = Regions.CONTROL_PANEL.x + 156, Regions.CONTROL_PANEL.y + 18
    PRAYER_TAB = Regions.CONTROL_PANEL.x + 189, Regions.CONTROL_PANEL.y + 18
    MAGIC_TAB = Regions.CONTROL_PANEL.x + 222, Regions.CONTROL_PANEL.y + 18

    CLAN_TAB = Regions.CONTROL_PANEL.x + 24, Regions.CONTROL_PANEL.y + 316
    FRIEND_TAB = Regions.CONTROL_PANEL.x + 57, Regions.CONTROL_PANEL.y + 316
    IGNORE_TAB = Regions.CONTROL_PANEL.x + 90, Regions.CONTROL_PANEL.y + 316
    LOGOUT_TAB = Regions.CONTROL_PANEL.x + 123, Regions.CONTROL_PANEL.y + 316
    OPTIONS_TAB = Regions.CONTROL_PANEL.x + 156, Regions.CONTROL_PANEL.y + 316
    EMOTE_TAB = Regions.CONTROL_PANEL.x + 189, Regions.CONTROL_PANEL.y + 316
    MUSIC_TAB = Regions.CONTROL_PANEL.x + 222, Regions.CONTROL_PANEL.y + 316

    BANK_CLOSE = Regions.BANK.x + 470, Regions.BANK.y + 17


class Minimap(Enum):
    COMPASS = Regions.MINIMAP.x + 54, Regions.MINIMAP.y + 20
    HEALTH = Regions.MINIMAP.x + 39, Regions.MINIMAP.y + 58
    PRAYER = Regions.MINIMAP.x + 39, Regions.MINIMAP.y + 93
    RUN = Regions.MINIMAP.x + 50, Regions.MINIMAP.y + 126
    SPECIAL = Regions.MINIMAP.x + 73, Regions.MINIMAP.y + 151


# dx = 26, dy = 24
class StandardSpellbook(Enum):
    HOME_TELEPORT = Regions.CONTROL_PANEL.x + 45, Regions.CONTROL_PANEL.y + 48


# dx = 40, dy = 27
class ArceuusSpellbook(Enum):
    HOME_TELEPORT = Regions.CONTROL_PANEL.x + 45, Regions.CONTROL_PANEL.y + 48
    RESURRECT_GREATER_GHOST = Regions.CONTROL_PANEL.x + 84, Regions.CONTROL_PANEL.y + 212
    RESURRECT_GREATER_SKELETON = Regions.CONTROL_PANEL.x + 124, Regions.CONTROL_PANEL.y + 212
    RESURRECT_GREATER_ZOMBIE = Regions.CONTROL_PANEL.x + 164, Regions.CONTROL_PANEL.y + 212


# dx = 37, dy = 37
class Prayer(Enum):
    PROTECT_FROM_MAGIC = Regions.CONTROL_PANEL.x + 82, Regions.CONTROL_PANEL.y + 174
    PROTECT_FROM_MISSILES = Regions.CONTROL_PANEL.x + 119, Regions.CONTROL_PANEL.y + 174
    PROTECT_FROM_MELEE = Regions.CONTROL_PANEL.x + 156, Regions.CONTROL_PANEL.y + 174
    EAGLE_EYE = Regions.CONTROL_PANEL.x + 193, Regions.CONTROL_PANEL.y + 174
    MYSTIC_MIGHT = Regions.CONTROL_PANEL.x + 45, Regions.CONTROL_PANEL.y + 211
    PIETY = Regions.CONTROL_PANEL.x + 82, Regions.CONTROL_PANEL.y + 248


class BarrowsCoord(Enum):
    SPADE = Regions.CONTROL_PANEL.x + 53, Regions.CONTROL_PANEL.y + 52  # todo: replace usages with Inventory.ITEM_1_1
    REWARDS_CLOSE = Regions.REWARD.x + 218, Regions.REWARD.y + 18


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

    SEARCH_BUTTON = Regions.TP_MENU.x + 24, Regions.TP_MENU.y + 17
    SEARCH_FIRST_RESULT = Regions.TP_MENU.x + 217, Regions.TP_MENU.y + 52
    SEARCH_SECOND_RESULT = Regions.TP_MENU.x + 217, Regions.TP_MENU.y + 827
