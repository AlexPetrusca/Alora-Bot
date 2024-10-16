from src.actions.primitives.action import Action
from src.robot import robot
from src.robot.timing.timer import Timer
from src.vision import vision
from src.vision.coordinates import Inventory
from src.vision.regions import Regions


class GearSwitchAction(Action):
    def __init__(self, item_coords, condition_item=None):
        super().__init__()
        self.item_coords = item_coords
        self.condition_item = condition_item

    def first_tick(self):
        self.set_progress_message("Switching gear...")

    def tick(self, timing):
        timing.execute(lambda: robot.press('Space'))  # inventory

        if self.condition_item is not None:
            found = timing.execute_after(Timer.sec2tick(0.1), self.is_condition_item_present, capture_result=True)
            if found is False:
                return timing.abort()

        for x, y in self.item_coords:
            timing.execute_after(Timer.sec2tick(0.1), lambda: robot.click(Inventory.item(x, y)))
        return timing.complete()

    def is_condition_item_present(self):
        loc = vision.locate_image(vision.grab_region(Regions.INVENTORY), self.condition_item, 0.9, silent=True)
        return loc is not None

    def last_tick(self):
        pass


class GearSwitch:
    TWO_BY_THREE = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]
    FIRST_ROW = [(0, 0), (0, 1), (0, 2), (0, 3)]
    SECOND_ROW = [(1, 0), (1, 1), (1, 2), (1, 3)]
