from enum import Enum

from src.actions.primitives.action import Action
from src.robot import robot
from src.robot.timer import Timer
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import ControlPanel, Prayer, BarrowsActionCoord, RewardMenu
from src.vision.images import Images
from src.vision.regions import Regions


class BarrowBrother:
    AHRIM = 'A'
    KARIL = 'K'
    GUTHAN = 'G'
    DHAROK = 'D'
    VERAC = 'V'
    TORAG = 'T'


class BarrowAction(Action):
    def __init__(self, barrow, prayer=Prayer.PROTECT_FROM_MELEE, last=False):
        super().__init__()
        self.barrow = barrow
        self.prayer = prayer
        self.last = last
        self.available_img = Images.Barrows.AVAILABLE_LABELS[barrow]
        self.unavailable_img = Images.Barrows.UNAVAILABLE_LABELS[barrow]

        self.skip = False
        self.fight_over_tick = None

    def first_tick(self):
        self.set_progress_message(f"Routing to Barrow {self.barrow} ...")

    def tick(self):
        self.T.execute(self.navigate_to_barrow)

        if self.skip:
            return self.T.complete_after(Timer.sec2tick(8))

        self.T.execute_after(Timer.sec2tick(1), lambda: robot.click(ControlPanel.INVENTORY_TAB))  # open inventory
        self.T.execute_after(Timer.sec2tick(7), lambda: robot.click(BarrowsActionCoord.SPADE))  # enter barrow

        self.T.execute_after(Timer.sec2tick(3), lambda: (
            self.set_progress_message("Fighting..."),
            robot.click_contour(Color.YELLOW)  # click sarcophagus + fight
        ))

        self.T.execute_after(Timer.sec2tick(3), lambda: robot.click(ControlPanel.PRAYER_TAB))  # open prayer
        self.T.execute_after(Timer.sec2tick(0.5), lambda: robot.click(self.prayer))  # enable custom prayer
        self.T.execute_after(Timer.sec2tick(0.5), lambda: robot.click(Prayer.PIETY))  # enable piety

        # todo: replace with combat action
        if self.fight_over_tick is None:
            self.T.wait(Timer.sec2tick(3))
            self.T.interval(Timer.sec2tick(1), self.poll_fight_over)
        else:
            self.T.tick_offset = self.fight_over_tick  # todo: this ain't pretty

            self.T.execute_after(Timer.sec2tick(0.5), lambda: robot.click(Prayer.PIETY))  # disable piety
            self.T.execute_after(Timer.sec2tick(0.5), lambda: robot.click(self.prayer))  # disable custom prayer

            if self.last:
                self.T.execute_after(Timer.sec2tick(4), lambda: robot.click(RewardMenu.CLOSE))  # collect rewards
                return self.T.complete()
            else:
                self.T.execute_after(Timer.sec2tick(1), lambda: (
                    self.set_progress_message(f"Completed Barrow {self.barrow}"),
                    robot.click_contour(Color.MAGENTA)  # exit barrow
                ))
                return self.T.complete_after(Timer.sec2tick(6))

        return Action.Status.IN_PROGRESS

    def navigate_to_barrow(self):
        if not robot.click_image(self.available_img, region=Regions.MINIMAP):
            robot.click_image(self.unavailable_img, region=Regions.MINIMAP)
            self.skip = True

    def poll_fight_over(self):
        ocr = vision.read_damage_ui()
        print('DAMAGE_UI:', ocr)
        if ocr.startswith('0/'):
            self.fight_over_tick = self.tick_counter

    def last_tick(self):
        self.fight_over_tick = None
        self.skip = False
