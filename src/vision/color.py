from enum import Enum
import numpy as np
import cv2 as cv


class Color(Enum):
    BLACK = [0, 0, 0]
    RED = [0, 0, 255]
    GREEN = [0, 255, 0]
    BLUE = [255, 0, 0]
    CYAN = [255, 255, 0]
    MAGENTA = [255, 0, 255]
    YELLOW = [0, 255, 255]
    WHITE = [255, 255, 255]

    DEFAULT_VALUE = [170, 255, 0]
    HIGHLIGHTED_VALUE = [255, 0, 170]
    LOW_VALUE = [255, 178, 102]
    MEDIUM_VALUE = [153, 255, 153]
    HIGH_VALUE = [0, 150, 255]
    INSANE_VALUE = [178, 102, 255]

    def to_string(self):
        match self:
            case Color.BLACK:
                return 'black'
            case Color.RED:
                return 'red'
            case Color.GREEN:
                return 'green'
            case Color.BLUE:
                return 'blue'
            case Color.CYAN:
                return 'cyan'
            case Color.MAGENTA:
                return 'magenta'
            case Color.YELLOW:
                return 'yellow'
            case Color.WHITE:
                return 'white'
            case _:
                return ''


def get_color_limits(color, ht=0.99, st=0.9, vt=0.8):
    def clip(value, lower=0, upper=255):
        return lower if value < lower else upper if value > upper else value

    h, s, v = cv.cvtColor(np.uint8([[color]]), cv.COLOR_BGR2HSV)[0][0]
    dh, ds, dv = max(h, 255 - h), max(s, 255 - s), max(v, 255 - v)
    hl, hh = clip(h - dh * (1 - ht)), clip(h + dh * (1 - ht))
    sl, sh = clip(s - ds * (1 - st)), clip(s + ds * (1 - st))
    vl, vh = clip(v - dv * (1 - vt)), clip(v + dv * (1 - vt))
    return (hl, sl, vl), (hh, sh, vh)
