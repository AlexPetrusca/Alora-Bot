from enum import Enum

from src.actions.primitives.action import Action

from src.robot import robot
from src.robot.timing.timer import Timer
from src.vision.coordinates import Minimap
from src.vision.images import Images
from src.vision.regions import Regions


class Direction(Enum):
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'


class CalibrateAction(Action):
    def __init__(self, direction=Direction.NORTH):
        super().__init__()
        self.direction = direction
        self.direction_menu = Images.Menu.COMPASS_DIRECTIONS[self.direction.value]

    def first_tick(self):
        self.set_progress_message('Calibrating Camera...')

    def tick(self, timing):
        if self.direction == Direction.NORTH:
            timing.execute(lambda: robot.click(Minimap.COMPASS))
        else:
            timing.execute(lambda: robot.right_click(Minimap.COMPASS))
            timing.execute_after(Timer.sec2tick(0.1), lambda: robot.click_image(self.direction_menu, region=Regions.MINIMAP))
        timing.execute(lambda: robot.key_down('up'))
        timing.execute_after(Timer.sec2tick(2), lambda: robot.key_up('up'))
        return timing.complete()

    def last_tick(self):
        pass
