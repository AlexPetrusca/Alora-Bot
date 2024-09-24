import math

import numpy as np
import cv2 as cv
from pytesseract import pytesseract

from src.util.common import hide_ui, get_color_limits
from src.vision.color import Color


def grab_screen(sct):
    return np.array(sct.grab(sct.monitors[1]))


def grab_damage_ui(sct):
    return grab_screen(sct)[152:192, 12:264]


def grab_minimap(sct):
    return grab_screen(sct)[74:420, 2952:3394]


def grab_inventory(sct):
    return grab_screen(sct)[1568:2234, 2910:3392]


def grab_hover_action(sct):
    return grab_screen(sct)[74:114, 0:800]


def locate_image(haystack, needle, threshold=0.7):
    result = cv.matchTemplate(haystack, needle, cv.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv.minMaxLoc(result)
    print(max_val)
    if max_val >= threshold:
        return max_loc[0] + needle.shape[1] / 2, max_loc[1] + needle.shape[0] / 2
    else:
        return None


def locate_contour(haystack, color, area_threshold=750):
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
            contour_center = round(x + w / 2), round(y + h / 2)
            distance = math.dist(screen_center, contour_center)
            if distance < closest_distance:
                closest_distance = distance
                closest_position = contour_center
    return closest_position


def locate_ground_item(haystack, area_threshold=500):
    haystack = hide_ui(np.ndarray.copy(haystack))

    def find_item_by_color(color):
        # _, threshold = cv.threshold(hide_ui(haystack), 0, 255, cv.THRESH_BINARY)
        # hsv_threshold = cv.cvtColor(threshold, cv.COLOR_BGR2HSV)
        lower_limit, upper_limit = get_color_limits(color, 10, 150, 150)
        mask = cv.inRange(cv.cvtColor(haystack, cv.COLOR_BGR2HSV), lower_limit, upper_limit)

        closest_distance = 999999999
        closest_position = None
        screen_center = haystack.shape[1] / 2, haystack.shape[0] / 2
        contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv.contourArea(contour) > area_threshold:
                x, y, w, h = cv.boundingRect(contour)
                contour_center = round(x + w / 2), round(y + h / 2)
                distance = math.dist(screen_center, contour_center)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_position = contour_center
        return closest_position

        # lower_limit, upper_limit = get_color_limits(color, 10, 200, 200)
        # mask = cv.inRange(cv.cvtColor(haystack, cv.COLOR_BGR2HSV), lower_limit, upper_limit)
        # morph = cv.morphologyEx(mask, cv.MORPH_CLOSE, np.ones((10, 200), np.uint8))
        #
        # closest_distance = 999999999
        # closest_position = None
        # screen_center = haystack.shape[1] / 2, haystack.shape[0] / 2
        # contours, _ = cv.findContours(morph, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        # for contour in contours:
        #     if cv.contourArea(contour) > area_threshold:
        #         x, y, w, h = cv.boundingRect(contour)
        #         contour_center = round(x + w / 2), round(y + h)
        #         distance = math.dist(screen_center, contour_center)
        #         if distance < closest_distance:
        #             closest_distance = distance
        #             closest_position = contour_center
        # return closest_position

    insane_value_item = find_item_by_color(Color.INSANE_VALUE.value)
    if insane_value_item is not None:
        print("INSANE VALUE")
        return insane_value_item

    high_value_item = find_item_by_color(Color.HIGH_VALUE.value)
    if high_value_item is not None:
        print("HIGH VALUE")
        return high_value_item

    medium_value_item = find_item_by_color(Color.MEDIUM_VALUE.value)
    if medium_value_item is not None:
        print("MEDIUM VALUE")
        return medium_value_item

    low_value_item = find_item_by_color(Color.LOW_VALUE.value)
    if low_value_item is not None:
        print("LOW VALUE")
        return low_value_item

    highlighted_item = find_item_by_color(Color.HIGHLIGHTED_VALUE.value)
    if highlighted_item is not None:
        print("HIGHLIGHTED VALUE")
        return highlighted_item

    default_item = find_item_by_color(Color.DEFAULT_VALUE.value)
    if default_item is not None:
        print("DEFAULT VALUE")
        return default_item

    return None


def get_latest_chat(sct):
    chat_line_image = grab_screen(sct)[2106:2144, 14:994]
    return pytesseract.image_to_string(chat_line_image)
