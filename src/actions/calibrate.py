from src.actions.action import Action

from src.robot import robot
from src.vision.coordinates import Minimap


class CalibrateAction(Action):
    def first_tick(self):
        self.set_progress_message('Calibrating Camera...')

    def tick(self, t):
        if self.tick_counter == 0:
            robot.click(Minimap.COMPASS)
        elif self.tick_counter == Action.sec2tick(0.1):
            robot.key_down('up')
        elif self.tick_counter == Action.sec2tick(2):
            robot.key_up('up')
        elif self.tick_counter == Action.sec2tick(3):
            return Action.Status.COMPLETE
        return Action.Status.IN_PROGRESS

    def last_tick(self):
        pass
