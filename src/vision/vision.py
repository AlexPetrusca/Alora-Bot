import math

import numpy as np
import cv2 as cv
from pytesseract import pytesseract

from src.util.common import hide_ui, get_color_limits, get_color_limits
from src.vision.color import Color
from src.vision.coordinates import PLAYER_SCREEN_POS


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
    if max_val >= threshold:
        print(max_val)
        return max_loc[0] + needle.shape[1] / 2, max_loc[1] + needle.shape[0] / 2
    else:
        print("ERROR: locate_image failed with:", max_val)
        return None


def locate_contour(haystack, color, area_threshold=750, min_distance=0):
    if hasattr(color, 'value'):
        color = color.value

    hsv = hide_ui(cv.cvtColor(haystack, cv.COLOR_BGR2HSV))
    lower_limit, upper_limit = get_color_limits(color)
    mask = cv.inRange(hsv, lower_limit, upper_limit)

    closest_distance = 999999999
    closest_position = None
    contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv.contourArea(contour) > area_threshold:
            x, y, w, h = cv.boundingRect(contour)
            contour_center = round(x + w / 2), round(y + h / 2)
            distance = math.dist(PLAYER_SCREEN_POS, contour_center)
            if min_distance < distance < closest_distance:
                closest_distance = distance
                closest_position = contour_center

    return closest_position


def locate_ground_item(haystack, area_threshold=500):
    haystack = hide_ui(np.ndarray.copy(haystack))

    def locate_item_by_color(screenshot, color):
        hsv = hide_ui(cv.cvtColor(screenshot, cv.COLOR_BGR2HSV))
        lower_limit, upper_limit = get_color_limits(color)
        mask = cv.inRange(hsv, lower_limit, upper_limit)

        # enhancements
        mask = cv.blur(mask, (3, 3))
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, np.ones((2, 2), np.uint8))

        largest_area = area_threshold
        largest_position = None
        contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv.contourArea(contour)
            # area = w * h
            if area > largest_area:
                largest_area = area
                x, y, w, h = cv.boundingRect(contour)
                largest_position = round(x + w / 2), round(y + h / 2)

        return largest_position

    insane_value_item = locate_item_by_color(haystack, Color.INSANE_VALUE.value)
    if insane_value_item is not None:
        print("INSANE VALUE")
        return insane_value_item

    high_value_item = locate_item_by_color(haystack, Color.HIGH_VALUE.value)
    if high_value_item is not None:
        print("HIGH VALUE")
        return high_value_item

    medium_value_item = locate_item_by_color(haystack, Color.MEDIUM_VALUE.value)
    if medium_value_item is not None:
        print("MEDIUM VALUE")
        return medium_value_item

    low_value_item = locate_item_by_color(haystack, Color.LOW_VALUE.value)
    if low_value_item is not None:
        print("LOW VALUE")
        return low_value_item

    highlighted_item = locate_item_by_color(haystack, Color.HIGHLIGHTED_VALUE.value)
    if highlighted_item is not None:
        print("HIGHLIGHTED VALUE")
        return highlighted_item

    default_item = locate_item_by_color(haystack, Color.DEFAULT_VALUE.value)
    if default_item is not None:
        print("DEFAULT VALUE")
        return default_item

    return None


def read_text(haystack, config=""):
    grayscale = cv.cvtColor(haystack, cv.COLOR_BGR2GRAY)
    threshold = cv.threshold(grayscale, 120, 255, cv.THRESH_BINARY)[1]
    # dilation = cv.dilate(threshold, np.ones((1, 2), np.uint8), iterations=1)
    return pytesseract.image_to_string(threshold, config=config).strip()


def read_int(haystack):
    text = read_text(haystack, config="--psm 6")
    old_text = text
    text = text.replace('O', '0')
    text = text.replace('i', '1').replace('I', '1')
    text = text.replace('z', '2').replace('Z', '2').replace('&2', '2')
    text = text.replace('y', '4').replace('k', '4').replace('h', '4').replace('L', '4')
    text = text.replace('S', '5')
    text = text.replace('G', '6').replace('E', '6')
    text = text.replace('B8', '8').replace('B', '8').replace('a', '8')
    text = text.replace('g', '9')
    try:
        print("HP:", old_text, "-->", text)
        return int(text)
    except ValueError:
        print("ERROR: read_int failed with:", text)
        return -1


def read_latest_chat(sct):
    chat_line_image = grab_screen(sct)[2106:2144, 14:994]
    return pytesseract.image_to_string(chat_line_image).strip()
    # return read_text(grab_screen(sct)[2106:2144, 14:994])  # todo: use this instead


def read_hitpoints(sct):
    return read_int(grab_screen(sct)[188:212, 2978:3018])


def read_prayer_energy(sct):
    return read_int(grab_screen(sct)[256:280, 2978:3018])


def read_run_energy(sct):
    return read_int(grab_screen(sct)[320:344, 2996:3036])


def read_spec_energy(sct):
    return read_int(grab_screen(sct)[372:396, 3044:3084])
