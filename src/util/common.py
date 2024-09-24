import cv2 as cv
import numpy as np


def hide(img, p1, p2, color=(0, 0, 0)):
    return cv.rectangle(img, (2 * p1[0], 2 * p1[1]), (2 * p2[0], 2 * p2[1]), color, thickness=-1)


def hide_ui(img):
    hide(img, (1328, 40), (1453, 70))  # hide exp bar
    hide(img, (1455, 784), (1696, 1117))  # hide inventory
    hide(img, (0, 922), (520, 1117))  # hide chat
    hide(img, (1476, 37), (1697, 210))  # hide minimap
    hide(img, (0, 37), (221, 210))  # hide status ui
    hide(img, (0, 37), (400, 57))  # hide hover text
    hide(img, (1696, 37), (1728, 1117))  # hide runelite sidebar
    # hide(img, (1660, 45), (1697, 60))  # hide ping
    return img


def get_color_limits(color):
    if color == [0, 0, 0]:
        return (0, 0, 0), (255, 50, 0)
    elif color == [255, 255, 255]:
        return (0, 0, 255), (255, 50, 255)
    hsv_convert = cv.cvtColor(np.uint8([[color]]), cv.COLOR_BGR2HSV)
    hue = int(hsv_convert[0][0][0])
    return (hue - 10, 100, 100), (hue + 10, 255, 255)
