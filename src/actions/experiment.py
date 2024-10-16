from src.actions.primitives.action import Action
from src.robot import robot
from src.robot.timing.timer import Timer
from src.vision.coordinates import Inventory


class ExperimentAction(Action):
    def __init__(self):
        super().__init__()

    def first_tick(self):
        self.set_progress_message('Experimenting...')

    def tick(self, timing):
        for y in range(0, 7):
            for x in range(0, 4):
                timing.execute_after(Timer.sec2tick(1), lambda: robot.click(Inventory.item(y, x)))

        return timing.complete()

    def last_tick(self):
        pass
