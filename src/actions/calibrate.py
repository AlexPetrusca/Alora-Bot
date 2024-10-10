from src.actions.primitives.action import Action

from src.robot import robot
from src.robot.timer import Timer
from src.vision.coordinates import Minimap


class CalibrateAction(Action):
    def first_tick(self):
        self.set_progress_message('Calibrating Camera...')

    def tick(self, timing):
        timing.execute(lambda: robot.click(Minimap.COMPASS))
        timing.execute(lambda: robot.key_down('up'))
        timing.execute_after(Timer.sec2tick(2), lambda: robot.key_down('up'))
        return timing.complete_after(Timer.sec2tick(1))

    def last_tick(self):
        pass
