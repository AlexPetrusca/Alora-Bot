import cv2 as cv
import numpy as np


def hide(img, p1, p2, color=(0, 0, 0)):
    return cv.rectangle(img, (2 * p1[0], 2 * p1[1]), (2 * p2[0], 2 * p2[1]), color, thickness=-1)


def mask_ui(img):
    hide(img, (1328, 40), (1453, 70))  # hide exp bar
    hide(img, (1455, 784), (1696, 1117))  # hide item
    hide(img, (0, 922), (520, 1117))  # hide chat
    hide(img, (1476, 37), (1697, 210))  # hide minimap
    hide(img, (0, 37), (221, 210))  # hide status ui
    hide(img, (0, 37), (400, 57))  # hide hover text
    hide(img, (1696, 37), (1728, 1117))  # hide runelite sidebar
    # hide(img, (1660, 45), (1697, 60))  # hide ping
    return img


def get_color_limits(color, ht=0.99, st=0.9, vt=0.8):
    def clip(value, lower=0, upper=255):
        return lower if value < lower else upper if value > upper else value

    h, s, v = cv.cvtColor(np.uint8([[color]]), cv.COLOR_BGR2HSV)[0][0]
    dh, ds, dv = max(h, 255 - h), max(s, 255 - s), max(v, 255 - v)
    hl, hh = clip(h - dh * (1 - ht)), clip(h + dh * (1 - ht))
    sl, sh = clip(s - ds * (1 - st)), clip(s + ds * (1 - st))
    vl, vh = clip(v - dv * (1 - vt)), clip(v + dv * (1 - vt))
    return (hl, sl, vl), (hh, sh, vh)
