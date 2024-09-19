from src.actions.action import Action
import cv2 as cv
import numpy as np
import logging
import mss

from src.util import robot
from src.util.coordinates import Minimap


class CalibrateAction(Action):
    def __init__(self):
        1+1

    def first_tick(self):
        self.set_status('Calibrating Camera...')

    def tick(self, t):
        if self.tick_counter == 0:
            robot.click(Minimap.COMPASS.value)
        elif self.tick_counter == 1:
            robot.key_down('up')
        elif self.tick_counter == 20:
            robot.key_up('up')
        return self.tick_counter == Action.sec2tick(3)

    def last_tick(self):
        pass
