from enum import Enum

from src.vision.color import Color
from src.util.common import get_color_limits
import cv2 as cv
import numpy as np
import mss
import time


class DisplayType(Enum):
    DETECTION = 1
    THRESHOLD = 2
    RED_MASK = 3
    YELLOW_MASK = 4
    PURPLE_MASK = 5


class DebugDisplay:
    display_type = DisplayType.DETECTION
    sct = mss.mss()
    bot = None

    def __init__(self, bot):
        self.bot = bot

    def show(self, t):
        screenshot = np.array(self.sct.grab(self.sct.monitors[1]))
        hover_action_image = np.ndarray.copy(screenshot[74:114, 0:800])
        _, threshold = cv.threshold(screenshot, 0, 255, cv.THRESH_BINARY)
        hsv_threshold = cv.cvtColor(threshold, cv.COLOR_BGR2HSV)

        red_lower, red_upper = get_color_limits(Color.RED.value)
        red_mask = cv.inRange(hsv_threshold, red_lower, red_upper)

        contours, _ = cv.findContours(red_mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            for contour in contours:
                if cv.contourArea(contour) > 1000:
                    x, y, w, h = cv.boundingRect(contour)
                    cv.rectangle(screenshot, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

        yellow_lower, yellow_upper = get_color_limits(Color.YELLOW.value)
        yellow_mask = cv.inRange(hsv_threshold, yellow_lower, yellow_upper)

        contours, _ = cv.findContours(yellow_mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            for contour in contours:
                if cv.contourArea(contour) > 1000:
                    x, y, w, h = cv.boundingRect(contour)
                    cv.rectangle(screenshot, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

        purple_lower, purple_upper = get_color_limits(Color.MAGENTA.value)
        purple_mask = cv.inRange(hsv_threshold, purple_lower, purple_upper)

        contours, _ = cv.findContours(purple_mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            for contour in contours:
                if cv.contourArea(contour) > 1000:
                    x, y, w, h = cv.boundingRect(contour)
                    cv.rectangle(screenshot, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

        # compass = cv.imread('../resources/target/compass.png', cv.IMREAD_UNCHANGED)
        # x, y = vision.locate_image(screenshot, compass, 0.5)
        # cv.rectangle(screenshot, (round(x) - 5, round(y) - 5), (round(x) + 5, round(y) + 5), (0, 0, 255), -1)

        image = screenshot
        if self.display_type == DisplayType.DETECTION:
            image = screenshot
        elif self.display_type == DisplayType.THRESHOLD:
            image = threshold
        elif self.display_type == DisplayType.RED_MASK:
            image = red_mask
        elif self.display_type == DisplayType.YELLOW_MASK:
            image = yellow_mask
        elif self.display_type == DisplayType.PURPLE_MASK:
            image = purple_mask
        cv.putText(screenshot, f'FPS: {round(1 / (time.perf_counter() - t))}', (10, 50), cv.FONT_HERSHEY_SIMPLEX,
                   1, (0, 0, 255), 2, cv.LINE_AA)
        # cv.putText(screenshot, pytesseract.image_to_string(hover_action_image), (200, 50), cv.FONT_HERSHEY_SIMPLEX,
        #            1, (0, 0, 255), 2, cv.LINE_AA)
        cv.putText(image, self.bot.action_queue[0].status, (1000, 50), cv.FONT_HERSHEY_SIMPLEX,
                   1, (0, 0, 255), 2, cv.LINE_AA)
        cv.imshow('Bot Vision', image)

        key = cv.waitKey(1) & 0xFF
        if key == ord("1"):
            self.display_type = DisplayType.DETECTION
        elif key == ord("2"):
            self.display_type = DisplayType.THRESHOLD
        elif key == ord("3"):
            self.display_type = DisplayType.RED_MASK
        elif key == ord("4"):
            self.display_type = DisplayType.YELLOW_MASK
        elif key == ord("5"):
            self.display_type = DisplayType.PURPLE_MASK
        elif key == ord("q"):
            cv.destroyAllWindows()
            exit(1)
