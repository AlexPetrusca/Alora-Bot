from src.actions.primitives.action import Action
from src.actions.types.action_status import ActionStatus
from src.robot import robot
from src.robot.timing.timer import Timer
from src.vision import vision
from src.vision.coordinates import Inventory
from src.vision.regions import Regions
from src.vision.vision import grab_region, read_int, read_text


class ExperimentAction(Action):
    def __init__(self):
        super().__init__()

    def first_tick(self):
        self.set_progress_message('Experimenting...')

    def tick(self, timing):
        timing.interval(Timer.sec2tick(1), self.print_prayer)
        return ActionStatus.IN_PROGRESS

    def print_prayer(self):
        screenshot = grab_region(Regions.PRAYER)
        print("Prayer:", read_text(screenshot, config='--psm 6'), "-->", read_int(screenshot))

    def last_tick(self):
        pass
