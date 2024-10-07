import cv2
import mss

from src.actions.action import Action
from src.robot import robot
from src.robot.timer import Timer
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import ControlPanel, Prayer, BarrowsActionCoord, RewardMenu
from src.vision.regions import Regions


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
        self.available_img = cv2.imread(f"../resources/label/barrows/available/{self.barrow}.png", cv2.IMREAD_UNCHANGED)
        self.unavailable_img = cv2.imread(f"../resources/label/barrows/unavailable/{self.barrow}.png", cv2.IMREAD_UNCHANGED)

    def first_tick(self):
        self.set_progress_message(f"Routing to Barrow {self.barrow} ...")

    def tick(self, tick_counter):
        tick_offset = 0

        if tick_counter == tick_offset:
            if not robot.click_image(self.available_img, region=Regions.MINIMAP):
                robot.click_image(self.unavailable_img, region=Regions.MINIMAP)
                self.skip = True

        if self.skip and tick_counter == tick_offset + Timer.sec2tick(8):
            return Action.Status.COMPLETE

        tick_offset += Timer.sec2tick(1)
        if tick_counter == tick_offset:  # open inventory
            robot.click(ControlPanel.INVENTORY_TAB)
        tick_offset += Timer.sec2tick(7)
        if tick_counter == tick_offset:  # enter barrow
            robot.click(BarrowsActionCoord.SPADE)

        tick_offset += Timer.sec2tick(3)
        if tick_counter == tick_offset:  # click sarcophagus + fight
            self.set_progress_message("Fighting...")
            robot.click_contour(Color.YELLOW)

        tick_offset += Timer.sec2tick(3)
        if tick_counter == tick_offset:
            robot.click(ControlPanel.PRAYER_TAB)
        tick_offset += Timer.sec2tick(0.5)
        if tick_counter == tick_offset:
            robot.click(self.prayer)
        tick_offset += Timer.sec2tick(0.5)
        if tick_counter == tick_offset:
            robot.click(Prayer.PIETY)

        # todo: replace with combat action
        tick_offset += Timer.sec2tick(3)
        if tick_counter > tick_offset and self.fight_over_tick is None:
            if tick_counter % Timer.sec2tick(1) == 0:
                ocr = vision.read_damage_ui(mss.mss())
                if ocr.startswith('0/'):
                    self.fight_over_tick = tick_counter

        if self.fight_over_tick is not None:
            tick_offset = self.fight_over_tick

            tick_offset += Timer.sec2tick(0.5)
            if tick_counter == tick_offset:
                robot.click(Prayer.PIETY)
            tick_offset += Timer.sec2tick(0.5)
            if tick_counter == tick_offset:
                robot.click(self.prayer)

            tick_offset += Timer.sec2tick(1)
            if self.last:
                tick_offset += Timer.sec2tick(3)
                if tick_counter == tick_offset:
                    robot.click(RewardMenu.CLOSE)  # collect rewards
                    return Action.Status.COMPLETE
            elif tick_counter == tick_offset:
                self.set_progress_message(f"Completed Barrow {self.barrow}")
                robot.click_contour(Color.MAGENTA)  # exit barrow

            if tick_counter == tick_offset + Timer.sec2tick(5):
                return Action.Status.COMPLETE

        return Action.Status.IN_PROGRESS

    def last_tick(self):
        self.fight_over_tick = None
        self.skip = False
