import numpy as np
import cv2 as cv


def grab_screen(sct):
    return np.array(sct.grab(sct.monitors[1]))


def grab_minimap(sct):
    return grab_screen(sct)[74:420, 2952:3394]


def grab_inventory(sct):
    return grab_screen(sct)[1568:2234, 2910:3392]


def grab_hover_action(sct):
    return grab_screen(sct)[74:114, 0:800]


def locate_image(haystack, needle, threshold=0.7):
    result = cv.matchTemplate(haystack, needle, cv.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv.minMaxLoc(result)
    if max_val >= threshold:
        return max_loc[0] + needle.shape[1] / 2, max_loc[1] + needle.shape[0] / 2
    else:
        return None
