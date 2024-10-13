from src.actions.combat import CombatAction
from src.actions.prayer import PrayerAction
from src.actions.primitives.action import Action
from src.robot import robot
from src.robot.timing.timer import Timer
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

        self.combat_action = CombatAction(target=None)
        self.prayer_on_action = PrayerAction(self.prayer, Prayer.PIETY)
        self.prayer_off_action = PrayerAction(Prayer.PIETY, self.prayer)

    def first_tick(self):
        self.set_progress_message(f"Routing to Barrow {self.barrow} ...")

    def tick(self, timing):
        is_previously_completed = not timing.execute(self.navigate_to_barrow, capture_result=True)
        if is_previously_completed:
            return timing.complete_after(Timer.sec2tick(8))

        timing.execute_after(Timer.sec2tick(1), lambda: robot.click(ControlPanel.INVENTORY_TAB))  # open inventory
        timing.execute_after(Timer.sec2tick(7), lambda: robot.click(BarrowsActionCoord.SPADE))  # enter barrow

        timing.execute_after(Timer.sec2tick(3), lambda: (
            self.set_progress_message("Fighting..."),
            robot.click_contour(Color.YELLOW)  # click sarcophagus + fight
        ))

        timing.wait(Timer.sec2tick(3))
        timing.action(self.prayer_on_action)

        timing.wait(Timer.sec2tick(3))
        timing.action(self.combat_action)

        timing.action(self.prayer_off_action)

        if self.last:
            timing.execute_after(Timer.sec2tick(4), lambda: robot.click(RewardMenu.CLOSE))  # collect rewards
            return timing.complete()
        else:
            timing.execute_after(Timer.sec2tick(1), lambda: (
                self.set_progress_message(f"Completed Barrow {self.barrow}"),
                robot.click_contour(Color.MAGENTA)  # exit barrow
            ))
            return timing.complete_after(Timer.sec2tick(6))

    def navigate_to_barrow(self):
        if not robot.click_image(self.available_img, region=Regions.MINIMAP):
            robot.click_image(self.unavailable_img, region=Regions.MINIMAP)
            return False
        return True

    def last_tick(self):
        pass
