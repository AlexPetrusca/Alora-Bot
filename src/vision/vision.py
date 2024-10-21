import math
from enum import Enum

import numpy as np
import cv2 as cv
from pytesseract import pytesseract

from src.vision.color import Color, get_color_limits
from src.vision.coordinates import Player, Prayer
from src.vision.images import PrayerProtect
from src.vision.regions import Regions
from src.vision.screen import Screen


class ContourDetection(Enum):
    DISTANCE_CLOSEST = 0
    DISTANCE_FARTHEST = 1
    AREA_LARGEST = 2
    AREA_SMALLEST = 3


def grab_screen(hide_ui=False):
    screenshot = Screen.grab()
    return mask_ui(screenshot) if hide_ui else screenshot


def grab_region(region):
    return grab_screen()[region.as_slice()]


def read_latest_chat():
    return read_text(grab_region(Regions.LATEST_CHAT))


def read_combat_info():
    combat_info = read_text(grab_region(Regions.COMBAT_INFO), config='--psm 6')
    combat_info.replace('@', '0').replace('o', '0').replace('O', '0')
    return combat_info


def read_hitpoints():
    return read_int(grab_region(Regions.HITPOINTS))


def read_prayer_energy():
    return read_int(grab_region(Regions.PRAYER))


def read_run_energy():
    return read_int(grab_region(Regions.RUN_ENERGY))


def read_spec_energy():
    return read_int(grab_region(Regions.SPEC_ENERGY))


def is_status_active(status):
    return locate_image(grab_region(Regions.STATUS_BAR), status, 0.85) is not None


def get_my_prayer_protect():
    return get_prayer_protect(grab_region(Regions.PLAYER))[0]


def get_opponent_prayer_protect(opponent_color=Color.RED):
    screenshot = grab_screen()
    contour, _ = get_contour(screenshot, opponent_color)
    if contour is not None:
        x, y, w, h = cv.boundingRect(contour)
        if w > 50 and h > 50:
            y = y - 75 if (y - 75 >= 0) else 0
            mask_region(screenshot, Regions.PLAYER_MOVE_BOX)
            return get_prayer_protect(screenshot[y:(y + h + 150), x:(x + w)])[0]

    # print("get_opponent_prayer_protect: no opponent found")
    return None


def get_prayer_protect(haystack):
    protect_loc = locate_image(haystack, PrayerProtect.MAGIC, 0.9)
    if protect_loc is not None:
        return Prayer.PROTECT_FROM_MAGIC, protect_loc
    protect_loc = locate_image(haystack, PrayerProtect.MELEE, 0.9)
    if protect_loc is not None:
        return Prayer.PROTECT_FROM_MELEE, protect_loc
    protect_loc = locate_image(haystack, PrayerProtect.RANGED, 0.9)
    if protect_loc is not None:
        return Prayer.PROTECT_FROM_MISSILES, protect_loc
    return None, None


def get_contour(haystack, color, area_threshold=750, mode=ContourDetection.DISTANCE_CLOSEST):
    if hasattr(color, 'value'):
        color = color.value

    # todo: use of mask_ui implies that the haystack should be a full screen capture
    hsv = mask_ui(cv.cvtColor(haystack, cv.COLOR_BGR2HSV))
    lower_limit, upper_limit = get_color_limits(color)
    mask = cv.inRange(hsv, lower_limit, upper_limit)

    to_maximize = (mode == ContourDetection.DISTANCE_FARTHEST or mode == ContourDetection.AREA_LARGEST)
    opt_value = 0 if to_maximize else 1e10
    opt_contour = None
    contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        contour_area = cv.contourArea(contour)
        if contour_area > area_threshold:
            x, y, w, h = cv.boundingRect(contour)
            contour_center = round(x + w / 2), round(y + h / 2)

            if mode == ContourDetection.AREA_LARGEST or mode == ContourDetection.AREA_SMALLEST:
                value = contour_area
            else:  # mode == ContourMode.DISTANCE_FARTHEST or mode == ContourMode.DISTANCE_CLOSEST:
                px, py = Player.POSITION.value
                value = math.dist((2 * px, 2 * py), contour_center)

            if (to_maximize and value > opt_value) or (not to_maximize and value < opt_value):
                opt_value = value
                opt_contour = contour

    return opt_contour, opt_value


def locate_image(haystack, needle, threshold=0.7, half_scale=False, silent=False):
    if half_scale:
        haystack = cv.resize(haystack, (0, 0), fx=0.5, fy=0.5, interpolation=cv.INTER_NEAREST_EXACT)
        needle = cv.resize(needle, (0, 0), fx=0.5, fy=0.5, interpolation=cv.INTER_NEAREST_EXACT)

    result = cv.matchTemplate(haystack, needle, cv.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv.minMaxLoc(result)
    if max_val >= threshold:
        # if not silent:
        #     print(max_val)
        center_loc = max_loc[0] + needle.shape[1] / 2, max_loc[1] + needle.shape[0] / 2
        if half_scale:
            return 2 * center_loc[0], 2 * center_loc[1]
        else:
            return center_loc
    else:
        if not silent:
            print("ERROR: locate_image failed with:", max_val)
        return None


def locate_contour(haystack, color, area_threshold=750, mode=ContourDetection.DISTANCE_CLOSEST):
    contour, _ = get_contour(haystack, color, area_threshold, mode)
    if contour is not None:
        x, y, w, h = cv.boundingRect(contour)
        return round(x + w / 2), round(y + h / 2)
    else:
        return None


def locate_ground_item(haystack, area_threshold=250):
    # todo: use of mask_ui implies that the haystack should be a full screen capture
    haystack = mask_ui(np.ndarray.copy(haystack))

    def locate_item_by_color(screenshot, color):
        hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)
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
    blur = cv.blur(threshold, (2, 2))
    morph = cv.morphologyEx(blur, cv.MORPH_CLOSE, np.ones((2, 2), np.uint8))
    return pytesseract.image_to_string(morph, config=config).strip()


# todo: this needs to be better >.<
def read_int(haystack):
    text = read_text(haystack, config='--psm 6')
    old_text = text

    # replace alphabetic characters with closest numerals
    text = text.replace('.', '').replace('"', '').replace('%', '')
    text = text.replace('o', '0').replace('O', '0').replace('Q', '0')
    text = text.replace('i', '1').replace('l', '1').replace('L', '1').replace('I', '1')
    text = text.replace('z', '2').replace('Z', '2')
    text = text.replace('y', '4').replace('k', '4').replace('h', '4').replace('u', '4').replace('&', '4')
    text = text.replace('S', '5').replace('s', '5')
    text = text.replace('G', '6').replace('E', '6')
    text = text.replace('7?', '7').replace('?', '7')
    text = text.replace('B', '8')
    text = text.replace('a', '9').replace('g', '9').replace('q', '9')

    try:
        # print("HP:", old_text, "-->", text)
        return int(text)
    except ValueError:
        # print("ERROR: read_int failed with:", old_text, "-->", text)
        return -1  # don't assume we've died if we cant read hitpoints


def mask_region(img, region, color=Color.BLACK):
    if hasattr(color, 'value'):
        color = color.value

    p1 = (2 * region.x, 2 * region.y)
    p2 = (2 * (region.x + region.w), 2 * (region.y + region.h))
    return cv.rectangle(img, p1, p2, color, thickness=-1)


def mask_ui(img):
    mask_region(img, Regions.EXP_BAR)  # hide exp bar
    mask_region(img, Regions.CONTROL_PANEL)  # hide control panel
    mask_region(img, Regions.CHAT)  # hide chat
    mask_region(img, Regions.MINIMAP)  # hide minimap
    mask_region(img, Regions.STATUS_BAR)  # hide status ui
    mask_region(img, Regions.HOVER_ACTION)  # hide hover text
    mask_region(img, Regions.RUNELITE_SIDEBAR)  # hide runelite sidebar
    return img
