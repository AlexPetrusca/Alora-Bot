import cv2

from src.actions.action import Action
from src.util import vision, robot
from src.util.color import Color
from src.util.coordinates import Controls, Prayer

SPADE = 1512, 845


class BarrowAction(Action):
    barrow = None
    image = None
    prayer = True
    last = False

    def __init__(self, barrow, prayer=True, last=False):
        self.barrow = barrow
        self.image = cv2.imread(f"../resources/target/label/{self.barrow}.png", cv2.IMREAD_UNCHANGED)
        self.prayer = prayer
        self.last = last

    def first_tick(self):
        self.set_status(f"Routing to Barrow {self.barrow} ...")

    # 5, 57 to 134, 95 - combat bar
    def tick(self, t):
        if self.tick_counter == 0:  # move to barrow (8s)
            robot.click_image(self.image)  # todo: should only search in minimap
        if self.tick_counter == Action.sec2tick(1):  # open inventory todo: if inventory is already open, don't open it again
            robot.click(Controls.INVENTORY_TAB.value)
        if self.tick_counter == Action.sec2tick(8):  # enter barrow (4s)
            robot.click(SPADE)
        if self.prayer:
            if self.tick_counter == Action.sec2tick(9):  # todo: its annoying to change one of these timings because everything after has to be updated as well
                robot.click(Controls.PRAYER_TAB.value)
            if self.tick_counter == Action.sec2tick(10):
                robot.click(Prayer.PROTECT_FROM_MELEE.value)
        if self.tick_counter == Action.sec2tick(12):  # click sarcophagus + fight (50s)
            self.set_status("Fighting...")
            robot.click_outline(Color.YELLOW.value)
        if self.last:
            if self.tick_counter == Action.sec2tick(61):
                robot.click(922, 417)
        if self.tick_counter == Action.sec2tick(62):  # exit barrow (8s) todo: if last we dont need to do this
            self.set_status(f"Completed Barrow {self.barrow}")
            robot.click_outline(Color.PURPLE.value)
        if self.prayer:
            if self.tick_counter == Action.sec2tick(63):
                robot.click(Prayer.PROTECT_FROM_MELEE.value)
        return self.tick_counter == Action.sec2tick(66)

    def last_tick(self):
        pass
