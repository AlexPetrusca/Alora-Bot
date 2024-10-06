from enum import Enum
from time import time
import cv2 as cv
import numpy as np
import mss

from src.vision.color import get_color_limits


class DisplayType(Enum):
    DETECTION = 1
    THRESHOLD = 2
    RED_MASK = 3
    YELLOW_MASK = 4
    PURPLE_MASK = 5


COLOR_RED = [0, 0, 255]
COLOR_YELLOW = [0, 255, 255]
COLOR_PURPLE = [255, 0, 255]
display_type = DisplayType.DETECTION

with mss.mss() as sct:
    while True:
        last_time = time()

        screenshot = np.array(sct.grab(sct.monitors[1]))
        _, threshold = cv.threshold(screenshot, 0, 255, cv.THRESH_BINARY)
        hsv_threshold = cv.cvtColor(threshold, cv.COLOR_BGR2HSV)

        red_lower, red_upper = get_color_limits(COLOR_RED)
        red_mask = cv.inRange(hsv_threshold, red_lower, red_upper)

        contours, _ = cv.findContours(red_mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            for contour in contours:
                if cv.contourArea(contour) > 1000:
                    x, y, w, h = cv.boundingRect(contour)
                    cv.rectangle(screenshot, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

        yellow_lower, yellow_upper = get_color_limits(COLOR_YELLOW)
        yellow_mask = cv.inRange(hsv_threshold, yellow_lower, yellow_upper)

        contours, _ = cv.findContours(yellow_mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            for contour in contours:
                if cv.contourArea(contour) > 1000:
                    x, y, w, h = cv.boundingRect(contour)
                    cv.rectangle(screenshot, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

        purple_lower, purple_upper = get_color_limits(COLOR_PURPLE)
        purple_mask = cv.inRange(hsv_threshold, purple_lower, purple_upper)

        contours, _ = cv.findContours(purple_mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            for contour in contours:
                if cv.contourArea(contour) > 1000:
                    x, y, w, h = cv.boundingRect(contour)
                    cv.rectangle(screenshot, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

        if display_type == DisplayType.DETECTION:
            cv.imshow('Vision Bot', screenshot)
        elif display_type == DisplayType.THRESHOLD:
            cv.imshow('Vision Bot', threshold)
        elif display_type == DisplayType.RED_MASK:
            cv.imshow('Vision Bot', red_mask)
        elif display_type == DisplayType.YELLOW_MASK:
            cv.imshow('Vision Bot', yellow_mask)
        elif display_type == DisplayType.PURPLE_MASK:
            cv.imshow('Vision Bot', purple_mask)

        key = cv.waitKey(1) & 0xFF
        if key == ord("1"):
            display_type = DisplayType.DETECTION
        elif key == ord("2"):
            display_type = DisplayType.THRESHOLD
        elif key == ord("3"):
            display_type = DisplayType.RED_MASK
        elif key == ord("4"):
            display_type = DisplayType.YELLOW_MASK
        elif key == ord("5"):
            display_type = DisplayType.PURPLE_MASK
        elif key == ord("q"):
            cv.destroyAllWindows()
            break

        print(f"FPS: {1 / (time() - last_time)}")
