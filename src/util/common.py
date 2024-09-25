import cv2 as cv
import numpy as np


def hide(img, p1, p2, color=(0, 0, 0)):
    return cv.rectangle(img, (2 * p1[0], 2 * p1[1]), (2 * p2[0], 2 * p2[1]), color, thickness=-1)


def hide_ui(img):
    hide(img, (1328, 40), (1453, 70))  # hide exp bar
    hide(img, (1455, 784), (1696, 1117))  # hide item
    hide(img, (0, 922), (520, 1117))  # hide chat
    hide(img, (1476, 37), (1697, 210))  # hide minimap
    hide(img, (0, 37), (221, 210))  # hide status ui
    hide(img, (0, 37), (400, 57))  # hide hover text
    hide(img, (1696, 37), (1728, 1117))  # hide runelite sidebar
    # hide(img, (1660, 45), (1697, 60))  # hide ping
    return img


# todo move away from this one
def get_color_limits(color, ht=10, st=100, bt=100):
    if color == [255, 255, 255]:
        return (0, st, bt), (255, 20, 255)
    hsv_convert = cv.cvtColor(np.uint8([[color]]), cv.COLOR_BGR2HSV)
    hue = int(hsv_convert[0][0][0])
    return (hue - ht, st, bt), (hue + ht, 255, 255)


def get_color_limits_2(color, ht=0.98, st=0.8, bt=0.8):
    hsv = cv.cvtColor(np.uint8([[color]]), cv.COLOR_BGR2HSV)[0][0]
    hl, hh = ht * hsv[0], (2 - ht) * hsv[0]
    sl, sh = st * hsv[1], (2 - st) * hsv[1]
    bl, bh = bt * hsv[2], (2 - bt) * hsv[2]
    return (hl, sl, bl), (hh, sh, bh)
