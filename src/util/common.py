import cv2 as cv
import numpy as np
from src.vision.coordinates import ScreenRegion


# def hide(img, p1, p2, color=(0, 0, 0)):
#     return cv.rectangle(img, (2 * p1[0], 2 * p1[1]), (2 * p2[0], 2 * p2[1]), color, thickness=-1)


def mask(img, region, color=(0, 0, 0)):
    if hasattr(region, 'value'):
        region = region.value
    p1 = region[1].start, region[0].start
    p2 = region[1].stop, region[0].stop
    return cv.rectangle(img, p1, p2, color, thickness=-1)


def mask_ui(img):
    mask(img, ScreenRegion.EXP_BAR)  # hide exp bar
    mask(img, ScreenRegion.CONTROL_PANEL)  # hide control panel
    mask(img, ScreenRegion.CHAT)  # hide chat
    mask(img, ScreenRegion.MINIMAP)  # hide minimap
    mask(img, ScreenRegion.STATUS)  # hide status ui
    mask(img, ScreenRegion.HOVER_ACTION)  # hide hover text
    mask(img, ScreenRegion.RUNELITE_SIDEBAR)  # hide runelite sidebar
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
