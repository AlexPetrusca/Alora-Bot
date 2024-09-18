from src.actions.action import Action
import numpy as np
import logging
import pyautogui
import mss


class CalibrateAction(Action):
    sct = mss.mss()

    def __init__(self):
        1+1

    def first_tick(self):
        logging.info('CALIBRATING...')

    def tick(self, t):
        # screenshot = np.array(self.sct.grab(self.sct.monitors[1]))
        # print(self.tick_counter)
        return t > 3
