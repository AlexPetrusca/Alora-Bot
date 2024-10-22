from enum import Enum, nonmember

from src.vision.regions import Regions


# todo: coordinates should be specified in scaled XY (0.0-1.0, 0.0-1.0)
def scale_coord(x, y):
    if (Regions.SCREEN.w, Regions.SCREEN.h) == (1728, 1117):
        return x, y
    else:
        ratio_x = Regions.GAME.w / (1728 - Regions.RUNELITE_SIDEBAR.w)
        ratio_y = Regions.GAME.h / 1080
        return round(ratio_x * x), round(ratio_y * (y - 37))


class Player(Enum):
    POSITION = Regions.GAME.w // 2 + 4, Regions.GAME.y + Regions.GAME.h // 2 + 4


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


class Inventory(Enum):
    ITEM_0_0 = Regions.CONTROL_PANEL.offset(58, 61)
    ITEM_0_1 = Regions.CONTROL_PANEL.offset(100, 61)
    ITEM_0_2 = Regions.CONTROL_PANEL.offset(142, 61)
    ITEM_0_3 = Regions.CONTROL_PANEL.offset(184, 61)

    ITEM_1_0 = Regions.CONTROL_PANEL.offset(58, 97)
    ITEM_1_1 = Regions.CONTROL_PANEL.offset(100, 97)
    ITEM_1_2 = Regions.CONTROL_PANEL.offset(142, 97)
    ITEM_1_3 = Regions.CONTROL_PANEL.offset(184, 97)

    ITEM_2_0 = Regions.CONTROL_PANEL.offset(58, 133)
    ITEM_2_1 = Regions.CONTROL_PANEL.offset(100, 133)
    ITEM_2_2 = Regions.CONTROL_PANEL.offset(142, 133)
    ITEM_2_3 = Regions.CONTROL_PANEL.offset(184, 133)

    ITEM_3_0 = Regions.CONTROL_PANEL.offset(58, 169)
    ITEM_3_1 = Regions.CONTROL_PANEL.offset(100, 169)
    ITEM_3_2 = Regions.CONTROL_PANEL.offset(142, 169)
    ITEM_3_3 = Regions.CONTROL_PANEL.offset(184, 169)

    ITEM_4_0 = Regions.CONTROL_PANEL.offset(58, 205)
    ITEM_4_1 = Regions.CONTROL_PANEL.offset(100, 205)
    ITEM_4_2 = Regions.CONTROL_PANEL.offset(142, 205)
    ITEM_4_3 = Regions.CONTROL_PANEL.offset(184, 205)

    ITEM_5_0 = Regions.CONTROL_PANEL.offset(58, 241)
    ITEM_5_1 = Regions.CONTROL_PANEL.offset(100, 241)
    ITEM_5_2 = Regions.CONTROL_PANEL.offset(142, 241)
    ITEM_5_3 = Regions.CONTROL_PANEL.offset(184, 241)

    ITEM_6_0 = Regions.CONTROL_PANEL.offset(58, 277)
    ITEM_6_1 = Regions.CONTROL_PANEL.offset(100, 277)
    ITEM_6_2 = Regions.CONTROL_PANEL.offset(142, 277)
    ITEM_6_3 = Regions.CONTROL_PANEL.offset(184, 277)

    @classmethod
    def item(cls, y, x):
        return cls[f'ITEM_{y}_{x}']


class Minimap(Enum):
    COMPASS = Regions.MINIMAP.offset(54, 20)
    HEALTH_ORB = Regions.MINIMAP.offset(39, 58)
    PRAYER_ORB = Regions.MINIMAP.offset(39, 93)
    RUN_ORB = Regions.MINIMAP.offset(50, 126)
    SPECIAL_ORB = Regions.MINIMAP.offset(73, 151)


class BankMenu(Enum):
    PLACEHOLDER_TOGGLE = Regions.BANK.offset(350, 776)
    SEARCH = Regions.BANK.offset(388, 776)
    DEPOSIT_INVENTORY = Regions.BANK.offset(426, 776)
    DEPOSIT_WORN_ITEMS = Regions.BANK.offset(464, 776)
    CLOSE = Regions.BANK.offset(470, 17)


class RewardMenu(Enum):
    CLOSE = Regions.REWARD.offset(218, 18)


class TeleportMenu(Enum):
    SEARCH = Regions.TELEPORT_MENU.offset(24, 17)
    CLOSE = Regions.TELEPORT_MENU.offset(472, 17)
    FIRST_RESULT = Regions.TELEPORT_MENU.offset(217, 52)
    SECOND_RESULT = Regions.TELEPORT_MENU.offset(217, 82)


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


class BarrowsActionCoord(Enum):
    SPADE = Regions.CONTROL_PANEL.offset(53, 52)  # todo: replace usages with Inventory.ITEM_1_1


class CerberusActionCoord(Enum):
    WALK1 = scale_coord(850, 50)
    WALK2 = scale_coord(750, 90)
    WALK3 = scale_coord(850, 215)


class HealActionCoord(Enum):
    WALK1 = scale_coord(700, 302)
    PRAYER_ALTAR = scale_coord(1292, 68)
    HEALER = scale_coord(805, 520)
    BANK_CHEST = scale_coord(1080, 524)


class TeleportActionCoord(Enum):
    TELEPORT_WIZARD = scale_coord(695, 255)
