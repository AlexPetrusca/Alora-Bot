from enum import Enum
import mss

monitor = mss.mss().monitors[1]
IS_M2 = (monitor['width'], monitor['height']) == (1728, 1117)
TOP_GAP = 37 if IS_M2 else 0


class Region:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def as_slice(self):
        p0 = (self.x, self.y)
        p1 = (self.x + self.w, self.y + self.h)
        return slice(2 * p0[1], 2 * p1[1]), slice(2 * p0[0], 2 * p1[0])

    def offset(self, x, y):
        return self.x + x, self.y + y


class Regions:
    SCREEN = Region(0, 0, monitor['width'], monitor['height'])
    GAME = Region(SCREEN.x, SCREEN.y + TOP_GAP, SCREEN.w - 30, SCREEN.h - TOP_GAP)
    RUNELITE_SIDEBAR = Region(GAME.x + GAME.w, GAME.y, 30, GAME.h)

    STATUS = Region(GAME.x, GAME.y, 221, 173)
    DAMAGE_UI = Region(STATUS.x + 8, STATUS.y + 40, 124, 16)
    HOVER_ACTION = Region(STATUS.x, STATUS.y, 400, 20)

    MINIMAP = Region(GAME.x + GAME.w - 215, GAME.y, 215, 172)
    HITPOINTS = Region(MINIMAP.x + 6, MINIMAP.y + 57, 20, 12)
    PRAYER = Region(MINIMAP.x + 6, MINIMAP.y + 91, 20, 12)
    RUN_ENERGY = Region(MINIMAP.x + 15, MINIMAP.y + 123, 20, 12)
    SPEC_ENERGY = Region(MINIMAP.x + 39, MINIMAP.y + 149, 20, 12)
    EXP_BAR = Region(MINIMAP.x - 153, MINIMAP.y + 2, 122, 30)

    CONTROL_PANEL = Region(GAME.x + GAME.w - 246, GAME.y + GAME.h - 334, 246, 334)

    CHAT = Region(GAME.x, GAME.y + GAME.h - 200, 520, 200)
    LATEST_CHAT = Region(CHAT.x + 7, CHAT.y + 136, 490, 18)

    BANK = Region(GAME.x + (GAME.w - 490) // 2, GAME.y + (GAME.h - 970) // 2, 488, 800)
    REWARD = Region(GAME.x + (GAME.w - 290) // 2, GAME.y + (GAME.h - 356) // 2, 234, 194)
    TELEPORT_MENU = Region(GAME.x + (GAME.w - 528) // 2, GAME.y + (GAME.h - 460) // 2, 488, 306)
