from src.actions.action import Action

from src.util import robot
from src.vision.coordinates import Minimap


class CalibrateAction(Action):
    def first_tick(self):
        self.set_status('Calibrating Camera...')

    def tick(self, t):
        if self.tick_counter == 0:
            robot.click(Minimap.COMPASS)
        elif self.tick_counter == 1:
            robot.key_down('up')
        elif self.tick_counter == Action.sec2tick(2):
            robot.key_up('up')
        return self.tick_counter == Action.sec2tick(3)

    def last_tick(self):
        pass
