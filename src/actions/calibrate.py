from src.actions.primitives.action import Action

from src.robot import robot
from src.robot.timer import Timer
from src.vision.coordinates import Minimap


class CalibrateAction(Action):
    def first_tick(self):
        self.set_progress_message('Calibrating Camera...')

    def tick(self, timing):
        if timing.tick_counter == 0:
            robot.click(Minimap.COMPASS)
        elif timing.tick_counter == Timer.sec2tick(0.1):
            robot.key_down('up')
        elif timing.tick_counter == Timer.sec2tick(2):
            robot.key_up('up')
        elif timing.tick_counter == Timer.sec2tick(3):
            return Action.Status.COMPLETE
        return Action.Status.IN_PROGRESS

    def last_tick(self):
        pass
