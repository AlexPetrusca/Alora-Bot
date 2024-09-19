import math

import numpy as np
import cv2 as cv

from src.util.common import hide_ui, get_color_limits


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

def locate_outline(haystack, color, area_threshold=750):
    _, threshold = cv.threshold(hide_ui(haystack), 0, 255, cv.THRESH_BINARY)
    hsv_threshold = cv.cvtColor(threshold, cv.COLOR_BGR2HSV)
    lower_limit, upper_limit = get_color_limits(color)
    mask = cv.inRange(hsv_threshold, lower_limit, upper_limit)

    closest_distance = 999999999
    closest_position = None
    screen_center = haystack.shape[1] / 2, haystack.shape[0] / 2
    contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv.contourArea(contour) > area_threshold:
            x, y, w, h = cv.boundingRect(contour)
            contour_center = x + w / 2, y + h / 2
            distance = math.dist(screen_center, contour_center)
            if distance < closest_distance:
                closest_distance = distance
                closest_position = contour_center
    return closest_position
