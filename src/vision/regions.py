from src.vision.screen import Screen


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

    def center(self):
        return self.x + self.w // 2, self.y + self.h // 2

    def offset(self, x, y):
        return self.x + x, self.y + y

    def global_px(self, x, y):
        return 2 * self.x + x, 2 * self.y + y

    def local_px(self, x, y):
        return x - 2 * self.x, y - 2 * self.y


class Regions:
    SCREEN = Region(0, 0, Screen.WIDTH, Screen.HEIGHT)
    GAME = Region(SCREEN.x, SCREEN.y + Screen.TOP_GAP, SCREEN.w - 30, SCREEN.h - Screen.TOP_GAP)
    RUNELITE_SIDEBAR = Region(GAME.x + GAME.w, GAME.y, 30, GAME.h)

    PLAYER = Region(GAME.w // 2 - 10 - 35, GAME.y + GAME.h // 2 - 20 - 50, 70, 100)  # todo: this region doesn't match exactly and the match is worse when the player is moving
    PLAYER_MOVE_BOX = Region(GAME.w // 2 - 10 - 100, GAME.y + GAME.h // 2 - 20 - 100, 200, 200)

    STATUS_BAR = Region(GAME.x, GAME.y, 221, 173)
    COMBAT_INFO = Region(STATUS_BAR.x + 8, STATUS_BAR.y + 40, 124, 16)
    HOVER_ACTION = Region(STATUS_BAR.x, STATUS_BAR.y, 400, 20)

    MINIMAP = Region(GAME.x + GAME.w - 215, GAME.y, 215, 172)
    HITPOINTS = Region(MINIMAP.x + 6, MINIMAP.y + 57, 20, 12)
    PRAYER = Region(MINIMAP.x + 6, MINIMAP.y + 91, 20, 12)
    RUN_ENERGY = Region(MINIMAP.x + 15, MINIMAP.y + 123, 20, 12)
    SPEC_ENERGY = Region(MINIMAP.x + 39, MINIMAP.y + 149, 20, 12)
    EXP_BAR = Region(MINIMAP.x - 153, MINIMAP.y + 2, 122, 30)

    CONTROL_PANEL = Region(GAME.x + GAME.w - 246, GAME.y + GAME.h - 334, 246, 334)
    INVENTORY = Region(CONTROL_PANEL.x + 39, CONTROL_PANEL.y + 43, 168, 253)

    CHAT = Region(GAME.x, GAME.y + GAME.h - 200, 520, 200)
    LATEST_CHAT = Region(CHAT.x + 7, CHAT.y + 136, 490, 18)

    BANK = Region(GAME.x + (GAME.w - 490) // 2, GAME.y + (GAME.h - 970) // 2, 488, 800)
    REWARD = Region(GAME.x + (GAME.w - 290) // 2, GAME.y + (GAME.h - 356) // 2, 234, 194)
    TELEPORT_MENU = Region(GAME.x + (GAME.w - 528) // 2, GAME.y + (GAME.h - 460) // 2, 488, 306)

    @classmethod
    def INVENTORY_ITEM(cls, x, y):
        return Region(cls.INVENTORY.x + 42 * x, cls.INVENTORY.y + 36 * y, 42, 36)
