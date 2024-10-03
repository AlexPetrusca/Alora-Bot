from enum import Enum
import mss

monitor = mss.mss().monitors[1]

M2_WIDTH = 1728
M2_HEIGHT = 1117
M2_TOP_OFFSET = 37
IS_M2 = (monitor['width'] == M2_WIDTH)

SCREEN_WIDTH = monitor['width']
SCREEN_HEIGHT = monitor['height']
SCREEN_TOP = M2_TOP_OFFSET if IS_M2 else 0
SCREEN_LEFT = 0

RUNELITE_SIDEBAR_WIDTH = 30
GAME_LEFT = SCREEN_LEFT
GAME_TOP = SCREEN_TOP
GAME_WIDTH = SCREEN_WIDTH - RUNELITE_SIDEBAR_WIDTH
GAME_HEIGHT = SCREEN_HEIGHT - SCREEN_TOP

# todo: below should be converted to enum

BANK_BOTTOM_OFFSET = 170
BANK_WIDTH = 490
BANK_HEIGHT = 800
BANK_LEFT = SCREEN_LEFT + (GAME_WIDTH - BANK_WIDTH) / 2
BANK_TOP = SCREEN_TOP + (GAME_HEIGHT - BANK_BOTTOM_OFFSET - BANK_HEIGHT) / 2

MINIMAP_WIDTH = 215
MINIMAP_HEIGHT = 172
MINIMAP_LEFT = SCREEN_LEFT + GAME_WIDTH - MINIMAP_WIDTH
MINIMAP_TOP = SCREEN_TOP

CONTROL_PANEL_WIDTH = 224
CONTROL_PANEL_HEIGHT = 334
CONTROL_PANEL_LEFT = SCREEN_LEFT + GAME_WIDTH - CONTROL_PANEL_WIDTH
CONTROL_PANEL_TOP = SCREEN_TOP + GAME_HEIGHT - CONTROL_PANEL_HEIGHT

CHAT_WIDTH = 520
CHAT_HEIGHT = 200
CHAT_LEFT = SCREEN_LEFT
CHAT_TOP = SCREEN_TOP + GAME_HEIGHT - CHAT_HEIGHT


# todo: coordinates should be specified in scaled XY (0.0-1.0, 0.0-1.0)
def rescale_coord(x, y):
    if SCREEN_WIDTH == M2_WIDTH:
        return x, y
    else:
        ratio_x = GAME_WIDTH / (M2_WIDTH - RUNELITE_SIDEBAR_WIDTH)
        ratio_y = GAME_HEIGHT / (M2_HEIGHT - M2_TOP_OFFSET)
        return round(ratio_x * x), round(ratio_y * (y - M2_TOP_OFFSET))


def slice2d(p0, p1):
    return slice(2 * p0[1], 2 * p1[1]), slice(2 * p0[0], 2 * p1[0])


class Player(Enum):
    POSITION = rescale_coord(855, 585)


# todo: express all as offsets
class Interface(Enum):
    MAGIC_TAB = rescale_coord(1674, 801)
    PRAYER_TAB = rescale_coord(1641, 801)
    EQUIPMENT_TAB = rescale_coord(1608, 801)
    INVENTORY_TAB = rescale_coord(1575, 801)
    QUEST_TAB = rescale_coord(1541, 801)
    STATS_TAB = rescale_coord(1508, 801)
    COMBAT_TAB = rescale_coord(1475, 801)
    # BANK_CLOSE = coord(1074, 110)
    BANK_CLOSE = BANK_LEFT + 470, BANK_TOP + 17


# todo: express all as offsets
class Minimap(Enum):
    COMPASS = rescale_coord(1535, 57)
    HEALTH = rescale_coord(1522, 95)
    PRAYER = rescale_coord(1522, 130)
    RUN = rescale_coord(1534, 162)
    SPECIAL = rescale_coord(1555, 187)


# todo: express all as offsets
class StandardSpellbook(Enum):
    HOME_TELEPORT = rescale_coord(1496, 832)


# todo: express all as offsets
class ArceuusSpellbook(Enum):
    HOME_TELEPORT = rescale_coord(1496, 832)
    RESURRECT_GREATER_SKELETON = rescale_coord(1575, 996)


# todo: express all as offsets
# x: 1496 - 1644  -->  5 columns  -->  37 gap
# y:  845 - 1030  -->  6 rows     -->  37 gap
class Prayer(Enum):
    PROTECT_FROM_MAGIC = rescale_coord(1533, 956)
    PROTECT_FROM_MISSILES = rescale_coord(1570, 956)
    PROTECT_FROM_MELEE = rescale_coord(1607, 956)
    EAGLE_EYE = rescale_coord(1644, 956)
    MYSTIC_MIGHT = rescale_coord(1496, 993)
    PIETY = rescale_coord(1533, 1030)


class BarrowsCoord(Enum):
    SPADE = rescale_coord(1512, 845)
    REWARDS_CLOSE = rescale_coord(922, 417)


class CerberusCoords(Enum):
    WALK1 = rescale_coord(850, 50)
    WALK2 = rescale_coord(750, 90)
    WALK3 = rescale_coord(850, 215)


class HealCoord(Enum):
    WALK1 = rescale_coord(700, 302)
    PRAYER_ALTAR = rescale_coord(1292, 68)
    HEALER = rescale_coord(805, 520)
    BANK_CHEST = rescale_coord(1080, 524)


# todo: All UI component coordinates must be scaled to resolution
# todo: express all as offsets
class TeleportCoord(Enum):
    TELEPORT_WIZARD = rescale_coord(695, 255)
    SEARCH_BUTTON = rescale_coord(608, 363)
    SEARCH_FIRST_RESULT = rescale_coord(800, 400)


class ScreenRegion(Enum):
    # DAMAGE_UI = slice2d(12, 152, 264, 192)
    DAMAGE_UI = slice2d(rescale_coord(6, 76), rescale_coord(132, 96))
