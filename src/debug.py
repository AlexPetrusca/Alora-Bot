from enum import Enum

from src.actions.pick_up_items import PickUpItemsAction
from src.actions.slayer import SlayerAction
from src.vision.color import Color
from src.util.common import hide_ui, get_color_limits
import cv2 as cv
import numpy as np
import mss
import time


class DebugDisplay:
    debug_tab = 1
    tab_name = ""

    sct = mss.mss()
    bot = None
    current_action = None

    def __init__(self, bot):
        self.bot = bot

    def show(self, t):
        screenshot = np.array(self.sct.grab(self.sct.monitors[1]))

        self.current_action = self.bot.action_queue[0]
        if isinstance(self.current_action, PickUpItemsAction):
            screenshot = self.show_pick_up_items(screenshot)
        elif isinstance(self.current_action, SlayerAction):
            screenshot = self.show_slayer(screenshot)
        else:
            screenshot = self.show_pick_up_items(screenshot)

        cv.putText(screenshot, f'FPS: {round(1 / (time.perf_counter() - t))}', (10, 50), cv.FONT_HERSHEY_SIMPLEX,
                   1, (0, 0, 255), 2, cv.LINE_AA)
        cv.putText(screenshot, self.bot.action_queue[0].status, (1000, 50), cv.FONT_HERSHEY_SIMPLEX,
                   1, (0, 0, 255), 2, cv.LINE_AA)
        cv.putText(screenshot, self.tab_name, (2000, 50), cv.FONT_HERSHEY_SIMPLEX,
                   1, (0, 0, 255), 2, cv.LINE_AA)
        cv.imshow('Bot Vision', screenshot)

        key = cv.waitKey(1) & 0xFF
        if ord("0") <= key <= ord("9"):
            self.debug_tab = key - ord("0")
        elif key == ord("q"):
            cv.destroyAllWindows()
            exit(1)

    def show_pick_up_items(self, screenshot):
        copy = hide_ui(cv.cvtColor(screenshot, cv.COLOR_BGR2HSV))
        if self.debug_tab == 1:
            self.tab_name = "Default Value Mask"
            lower_limit, upper_limit = get_color_limits(Color.DEFAULT_VALUE.value)
        elif self.debug_tab == 2:
            self.tab_name = "Highlighted Value Mask"
            lower_limit, upper_limit = get_color_limits(Color.HIGHLIGHTED_VALUE.value)
        elif self.debug_tab == 3:
            self.tab_name = "Low Value Mask"
            lower_limit, upper_limit = get_color_limits(Color.LOW_VALUE.value)
        elif self.debug_tab == 4:
            self.tab_name = "Medium Value Mask"
            lower_limit, upper_limit = get_color_limits(Color.MEDIUM_VALUE.value)
        elif self.debug_tab == 5:
            self.tab_name = "High Value Mask"
            lower_limit, upper_limit = get_color_limits(Color.HIGH_VALUE.value)
        elif self.debug_tab == 6:
            self.tab_name = "Insane Value Mask"
            lower_limit, upper_limit = get_color_limits(Color.INSANE_VALUE.value)
        else:
            self.tab_name = "Default Value Mask"
            lower_limit, upper_limit = get_color_limits(Color.DEFAULT_VALUE.value)

        mask = cv.inRange(copy, lower_limit, upper_limit)
        contours = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]
        mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
        for contour in contours:
            if cv.contourArea(contour) > 250:
                x, y, w, h = cv.boundingRect(contour)
                c = round(x + w / 2), round(y + h / 2)
                cv.rectangle(mask, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2, lineType=cv.LINE_AA)
                cv.rectangle(mask, (c[0] - 5, c[1] - 5), (c[0] + 5, c[1] + 5), color=(0, 0, 255), thickness=-1, lineType=cv.LINE_AA)

        return mask

    def show_slayer(self, screenshot):
        slayer_color = self.current_action.color

        screenshot = hide_ui(cv.cvtColor(screenshot, cv.COLOR_BGR2HSV))
        lower_limit, upper_limit = get_color_limits(slayer_color)
        mask = cv.inRange(screenshot, lower_limit, upper_limit)
        contours = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]
        mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
        for contour in contours:
            if cv.contourArea(contour) > 250:
                x, y, w, h = cv.boundingRect(contour)
                c = round(x + w / 2), round(y + h / 2)
                cv.rectangle(mask, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2, lineType=cv.LINE_AA)
                cv.rectangle(mask, (c[0] - 5, c[1] - 5), (c[0] + 5, c[1] + 5), color=(0, 0, 255), thickness=-1, lineType=cv.LINE_AA)

        return mask
