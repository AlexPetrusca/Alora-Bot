import cv2
import mss

from src.actions.primitives.action import Action
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

    def tick(self):
        self.execute(self.navigate_to_barrow)

        if self.skip:
            return self.complete_after(Timer.sec2tick(8))

        self.execute_after(Timer.sec2tick(1), lambda: robot.click(ControlPanel.INVENTORY_TAB))  # open inventory
        self.execute_after(Timer.sec2tick(7), lambda: robot.click(BarrowsActionCoord.SPADE))  # enter barrow

        self.execute_after(Timer.sec2tick(3), lambda: (
            self.set_progress_message("Fighting..."),
            robot.click_contour(Color.YELLOW)  # click sarcophagus + fight
        ))

        self.execute_after(Timer.sec2tick(3), lambda: robot.click(ControlPanel.PRAYER_TAB))  # open prayer
        self.execute_after(Timer.sec2tick(0.5), lambda: robot.click(self.prayer))  # enable custom prayer
        self.execute_after(Timer.sec2tick(0.5), lambda: robot.click(Prayer.PIETY))  # enable piety

        # todo: replace with combat action
        if self.fight_over_tick is None:
            self.wait(Timer.sec2tick(3))
            self.interval(Timer.sec2tick(1), self.poll_fight_over)
        else:
            self.tick_offset = self.fight_over_tick  # todo: this ain't pretty

            self.execute_after(Timer.sec2tick(0.5), lambda: robot.click(Prayer.PIETY))  # disable piety
            self.execute_after(Timer.sec2tick(0.5), lambda: robot.click(self.prayer))  # disable custom prayer

            if self.last:
                self.execute_after(Timer.sec2tick(4), lambda: robot.click(RewardMenu.CLOSE))  # collect rewards
                return self.complete()
            else:
                self.execute_after(Timer.sec2tick(1), lambda: (
                    self.set_progress_message(f"Completed Barrow {self.barrow}"),
                    robot.click_contour(Color.MAGENTA)  # exit barrow
                ))
                return self.complete_after(Timer.sec2tick(6))

        return Action.Status.IN_PROGRESS

    def navigate_to_barrow(self):
        if not robot.click_image(self.available_img, region=Regions.MINIMAP):
            robot.click_image(self.unavailable_img, region=Regions.MINIMAP)
            self.skip = True

    def poll_fight_over(self):
        ocr = vision.read_damage_ui(mss.mss())
        print('DAMAGE_UI:', ocr)
        if ocr.startswith('0/'):
            self.fight_over_tick = self.tick_counter

    def last_tick(self):
        self.fight_over_tick = None
        self.skip = False
