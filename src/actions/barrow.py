import cv2
import mss
from pytesseract import pytesseract

from src.actions.action import Action
from src.robot import robot
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import ControlPanel, Prayer, BarrowsActionCoord, RewardMenu


class BarrowAction(Action):
    barrow = None
    prayer = None
    last = False
    available_img = None
    unavailable_img = None

    skip = False
    fight_over_tick = None

    def __init__(self, barrow, prayer=Prayer.PROTECT_FROM_MELEE, last=False):
        self.barrow = barrow
        self.prayer = prayer
        self.last = last
        self.available_img = cv2.imread(f"../resources/target/label/barrows/available/{self.barrow}.png", cv2.IMREAD_UNCHANGED)
        self.unavailable_img = cv2.imread(f"../resources/target/label/barrows/unavailable/{self.barrow}.png", cv2.IMREAD_UNCHANGED)

    def first_tick(self):
        self.set_status(f"Routing to Barrow {self.barrow} ...")

    def tick(self, t):
        if self.tick_counter == 0:  # move to barrow (8s)
            # todo: [important] should only search in minimap
            if not robot.click_image(self.available_img, 0.94):
                robot.click_image(self.unavailable_img, 0.94)
                self.skip = True

        if self.skip:
            return self.tick_counter == Action.sec2tick(8)

        if self.tick_counter == Action.sec2tick(1):  # open inventory
            robot.click(ControlPanel.INVENTORY_TAB)
        if self.tick_counter == Action.sec2tick(8):  # enter barrow (4s)
            robot.click(BarrowsActionCoord.SPADE)

        if self.tick_counter == Action.sec2tick(11):  # click sarcophagus + fight (50s)
            self.set_status("Fighting...")
            robot.click_contour(Color.YELLOW)

        if self.tick_counter == Action.sec2tick(14):  # todo: its annoying to change one of these timings because everything after has to be updated as well
            robot.click(ControlPanel.PRAYER_TAB)
        if self.tick_counter == Action.sec2tick(14.5):
            robot.click(self.prayer)
        if self.tick_counter == Action.sec2tick(15):
            robot.click(Prayer.PIETY)

        if self.tick_counter > Action.sec2tick(18) and self.fight_over_tick is None:
            if self.tick_counter % Action.sec2tick(1) == 0:
                damage_ui = vision.grab_damage_ui(mss.mss())
                ocr = pytesseract.image_to_string(damage_ui).strip()
                print(ocr)
                if ocr.startswith('0/') or ocr.startswith('o/'):  # todo: checking 'o/' ain't pretty
                    self.fight_over_tick = self.tick_counter

        if self.fight_over_tick is not None:
            if self.tick_counter == self.fight_over_tick + Action.sec2tick(0.5):
                robot.click(Prayer.PIETY)
            if self.tick_counter == self.fight_over_tick + Action.sec2tick(1):
                robot.click(self.prayer)

            # if self.last and self.tick_counter == self.fight_over_tick + Action.sec2tick(2):  # todo: this is being done too early
            #     print("COLLECTING REWARDS")
            #     robot.click(BarrowsCoords.REWARDS_CLOSE)  # collect rewards
            if self.last:
                if self.tick_counter == self.fight_over_tick + Action.sec2tick(5):
                    robot.click(RewardMenu.CLOSE)  # collect rewards
                    return True
            elif self.tick_counter == self.fight_over_tick + Action.sec2tick(2):
                self.set_status(f"Completed Barrow {self.barrow}")
                robot.click_contour(Color.MAGENTA)  # exit barrow (8s) todo: if last we dont need to do this

            return self.tick_counter == self.fight_over_tick + Action.sec2tick(7)

        return False

    def last_tick(self):
        self.fight_over_tick = None
        self.skip = False
