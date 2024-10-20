from src.actions.primitives.action import Action
from src.actions.types.action_status import ActionStatus
from src.robot import robot
from src.robot.timing.timer import Timer
from src.vision import vision
from src.vision.coordinates import Inventory, Prayer, ControlPanel
from src.vision.regions import Regions
from src.vision.vision import grab_region, read_int, read_text


class ExperimentAction(Action):
    def __init__(self):
        super().__init__()
        self.counter = ExperimentAction.create_counter()

    def first_tick(self):
        self.set_progress_message('Experimenting...')

    def tick(self, timing):
        """ OCR on Prayer Points """
        # timing.interval(Timer.sec2tick(1), self.print_prayer)

        """ Parallel Clicks """
        def action1():
            timing.acquire_mouse()
            timing.execute(lambda: robot.click(ControlPanel.INVENTORY_TAB))
            timing.execute_after(Timer.sec2tick(1), lambda: robot.click(Prayer.PROTECT_FROM_MELEE))
            timing.release_mouse()

        def action2():
            timing.acquire_mouse()
            timing.execute(lambda: robot.click(ControlPanel.PRAYER_TAB))
            timing.execute_after(Timer.sec2tick(0.5), lambda: robot.click(Prayer.PROTECT_FROM_MISSILES))
            timing.release_mouse()

        timing.observe(Timer.sec2tick(5), self.counter, action1)
        timing.observe(Timer.sec2tick(5), self.counter, action2)

        return ActionStatus.IN_PROGRESS

    def print_prayer(self):
        screenshot = grab_region(Regions.PRAYER)
        print("Prayer:", read_text(screenshot, config='--psm 6'), "-->", read_int(screenshot))

    @staticmethod
    def create_counter(count=0):
        def increment():
            nonlocal count
            count += 1
            return count

        return increment

    def last_tick(self):
        pass
