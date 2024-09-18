import pyautogui

from src.actions.action import Action
import cv2 as cv
import numpy as np
import logging
import mss

class CalibrateAction(Action):
    sct = mss.mss()

    def __init__(self):
        1+1

    def first_tick(self):
        logging.info('CALIBRATING...')

    def tick(self, t):
        if self.tick_counter == 0:
            pyautogui.click(1535, 57)
        elif self.tick_counter == 1:
            pyautogui.keyDown('up')
        elif self.tick_counter == 20:
            pyautogui.keyUp('up')
        return self.tick_counter == Action.sec2tick(3)

    def last_tick(self):
        pass
