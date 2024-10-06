import cv2 as cv
import numpy as np

from src.vision.regions import Regions


def mask(img, region, color=(0, 0, 0)):
    p1 = (2 * region.x, 2 * region.y)
    p2 = (2 * (region.x + region.w), 2 * (region.y + region.h))
    return cv.rectangle(img, p1, p2, color, thickness=-1)


def mask_ui(img):
    mask(img, Regions.EXP_BAR)  # hide exp bar
    mask(img, Regions.CONTROL_PANEL)  # hide control panel
    mask(img, Regions.CHAT)  # hide chat
    mask(img, Regions.MINIMAP)  # hide minimap
    mask(img, Regions.STATUS)  # hide status ui
    mask(img, Regions.HOVER_ACTION)  # hide hover text
    mask(img, Regions.RUNELITE_SIDEBAR)  # hide runelite sidebar
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
