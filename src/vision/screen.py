import numpy as np
from mss import mss


class Screen:
    SCT = mss()
    WIDTH = SCT.monitors[1]['width']
    HEIGHT = SCT.monitors[1]['height']
    IS_M2 = (WIDTH, HEIGHT) == (1728, 1117)
    TOP_GAP = 37 if IS_M2 else 0

    @staticmethod
    def grab():
        monitor = Screen.SCT.monitors[1]
        return np.array(Screen.SCT.grab(monitor))
