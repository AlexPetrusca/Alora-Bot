from src.actions.primitives.action import Action
from src.robot import robot
from src.robot.timing.timer import Timer
from src.vision.coordinates import Inventory


class GearSwitchAction(Action):
    def __init__(self, *item_coords):
        super().__init__()
        self.item_coords = item_coords

    def first_tick(self):
        self.set_progress_message("Switching gear...")

    def tick(self, timing):
        for x, y in self.item_coords:
            timing.execute_after(Timer.sec2tick(0.1), lambda: robot.click(Inventory.item(x, y)))
        return timing.complete()

    def last_tick(self):
        pass
