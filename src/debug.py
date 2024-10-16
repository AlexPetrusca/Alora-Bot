from concurrent.futures import ThreadPoolExecutor
from time import perf_counter

import cv2 as cv
import numpy as np

from src.actions.pick_up_items import PickUpItemsAction
from src.actions.combat import CombatAction
from src.actions.tormented_demon import TormentedDemonAction
from src.actions.zulrah import ZulrahAction
from src.vision import vision
from src.vision.color import Color, get_color_limits
from src.vision.regions import Regions
from src.vision.vision import ContourDetection, mask_ui

executor = ThreadPoolExecutor()


class DebugDisplay:
    def __init__(self, bot):
        self.bot = bot

        self.debug_tab = 1
        self.tab_name = ''
        self.debug_text = ''

    def run(self):
        t_start = perf_counter()

        screenshot = vision.grab_screen()
        if isinstance(self.bot.current_action, PickUpItemsAction):
            screenshot = self.tick_pick_up_items(screenshot)
        elif isinstance(self.bot.current_action, CombatAction):
            screenshot = self.tick_slayer(screenshot)
        elif isinstance(self.bot.current_action, ZulrahAction):
            screenshot = self.tick_zulrah(screenshot)
        elif isinstance(self.bot.current_action, TormentedDemonAction):
            screenshot = self.tick_tormented_demon(screenshot)
        else:
            screenshot = self.tick_default(screenshot)

        t_end = perf_counter()

        cv.putText(screenshot, f'FPS: {round(1 / (t_start - t_end))}', (10, 50), cv.FONT_HERSHEY_SIMPLEX,
                   1, (0, 0, 255), 2, cv.LINE_AA)
        cv.putText(screenshot, self.bot.action_queue[0].progress_message, (1000, 50), cv.FONT_HERSHEY_SIMPLEX,
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

    def tick_pick_up_items(self, screenshot):
        copy = mask_ui(cv.cvtColor(screenshot, cv.COLOR_BGR2HSV))
        screenshot = cv.cvtColor(cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY), cv.COLOR_GRAY2BGR)

        def identify_items(color, return_mask=True):
            lower_limit, upper_limit = get_color_limits(color)
            mask = cv.inRange(copy, lower_limit, upper_limit)

            # enhancements
            mask = cv.blur(mask, (3, 3))
            mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, np.ones((2, 2), np.uint8))

            contours = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]
            mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
            target = mask if return_mask else screenshot

            for contour in contours:
                if cv.contourArea(contour) > 250:
                    x, y, w, h = cv.boundingRect(contour)
                    c = round(x + w / 2), round(y + h / 2)
                    cv.rectangle(target, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2, lineType=cv.LINE_AA)
                    cv.rectangle(target, (c[0] - 5, c[1] - 5), (c[0] + 5, c[1] + 5), color=(0, 0, 255), thickness=-1,
                                 lineType=cv.LINE_AA)

            return target

        if self.debug_tab == 1:
            self.tab_name = "All Item Values"
            identify_items(Color.DEFAULT_VALUE.value, False)
            identify_items(Color.LOW_VALUE.value, False)
            identify_items(Color.MEDIUM_VALUE.value, False)
            identify_items(Color.HIGH_VALUE.value, False)
            identify_items(Color.INSANE_VALUE.value, False)
            return identify_items(Color.HIGHLIGHTED_VALUE.value, False)
        if self.debug_tab == 2:
            self.tab_name = "Default Value Mask"
            return identify_items(Color.DEFAULT_VALUE.value)
        elif self.debug_tab == 3:
            self.tab_name = "Low Value Mask"
            return identify_items(Color.LOW_VALUE.value)
        elif self.debug_tab == 4:
            self.tab_name = "Medium Value Mask"
            return identify_items(Color.MEDIUM_VALUE.value)
        elif self.debug_tab == 5:
            self.tab_name = "High Value Mask"
            return identify_items(Color.HIGH_VALUE.value)
        elif self.debug_tab == 6:
            self.tab_name = "Insane Value Mask"
            return identify_items(Color.INSANE_VALUE.value)
        elif self.debug_tab == 7:
            self.tab_name = "Highlighted Value Mask"
            return identify_items(Color.HIGHLIGHTED_VALUE.value)
        else:
            self.debug_tab = 1
            return self.tick_pick_up_items(screenshot)

    def tick_slayer(self, screenshot):
        slayer_color = self.bot.current_action.target

        screenshot = mask_ui(cv.cvtColor(screenshot, cv.COLOR_BGR2HSV))
        lower_limit, upper_limit = get_color_limits(slayer_color)
        mask = cv.inRange(screenshot, lower_limit, upper_limit)
        contours = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]
        mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
        for contour in contours:
            if cv.contourArea(contour) > 750:
                x, y, w, h = cv.boundingRect(contour)
                c = round(x + w / 2), round(y + h / 2)
                cv.rectangle(mask, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2, lineType=cv.LINE_AA)
                cv.rectangle(mask, (c[0] - 5, c[1] - 5), (c[0] + 5, c[1] + 5), color=(0, 0, 255), thickness=-1,
                             lineType=cv.LINE_AA)

        return mask

    def tick_zulrah(self, screenshot):
        if self.debug_tab == 1:
            self.tab_name = "Zulrah Markers"
        if self.debug_tab == 2:
            self.tab_name = "Green Mask"
            return self.get_color_mask(screenshot, Color.GREEN.value)
        elif self.debug_tab == 3:
            self.tab_name = "Blue Mask"
            return self.get_color_mask(screenshot, Color.BLUE.value)
        elif self.debug_tab == 4:
            self.tab_name = "Red Mask"
            return self.get_color_mask(screenshot, Color.RED.value)

        red_contour, red_area = vision.get_contour(screenshot, Color.RED, mode=ContourDetection.AREA_LARGEST)
        green_contour, green_area = vision.get_contour(screenshot, Color.GREEN, mode=ContourDetection.AREA_LARGEST)
        blue_contour, blue_area = vision.get_contour(screenshot, Color.BLUE, mode=ContourDetection.AREA_LARGEST)

        if red_contour is not None:
            x, y, w, h = cv.boundingRect(red_contour)
            red_loc = round(x + w / 2), round(y + h / 2)
            DebugDisplay.draw_point(screenshot, red_loc[0], red_loc[1], Color.MAGENTA.value, 10, f'{red_area}')
        if green_contour is not None:
            x, y, w, h = cv.boundingRect(green_contour)
            green_loc = round(x + w / 2), round(y + h / 2)
            DebugDisplay.draw_point(screenshot, green_loc[0], green_loc[1], Color.YELLOW.value, 10, f'{green_area}')
        if blue_contour is not None:
            x, y, w, h = cv.boundingRect(blue_contour)
            blue_loc = round(x + w / 2), round(y + h / 2)
            DebugDisplay.draw_point(screenshot, blue_loc[0], blue_loc[1], Color.CYAN.value, 10, f'{blue_area}')

        return screenshot

    def tick_tormented_demon(self, screenshot):
        self.tab_name = "Tormented Demon Detection"

        screenshot = vision.mask_region(screenshot, Regions.PLAYER_MOVE_BOX)

        contour, _ = vision.get_contour(screenshot, Color.RED)
        if contour is not None:
            x, y, w, h = cv.boundingRect(contour)
            if w > 50 and h > 50:
                y = y - 75 if (y - 75 >= 0) else 0
                cv.rectangle(screenshot, (x, y), (x + w, y + h + 150), color=(0, 255, 0), thickness=2)

        return screenshot

    def tick_default(self, screenshot):
        self.tab_name = "Default Display"

        def update_debug_info():
            latest_chat = vision.read_text(screenshot[Regions.LATEST_CHAT.as_slice()], config='--psm 6')
            hitpoints_text = vision.read_text(screenshot[Regions.HITPOINTS.as_slice()], config='--psm 6')
            hitpoints_int = vision.read_int(screenshot[Regions.HITPOINTS.as_slice()])
            damage_ui = vision.read_text(screenshot[Regions.COMBAT_INFO.as_slice()], config='--psm 6')

            hitpoints = f'[Hitpoints]: {hitpoints_text} -> {hitpoints_int}'
            damage_ui = f'[Damage Ui]: {damage_ui}'
            latest_chat = f'[Latest Chat]: {latest_chat}'
            self.debug_text = f'{hitpoints}\n{damage_ui}\n{latest_chat}'

        if self.bot.timer.tick_counter % 10 == 0:  # every second
            executor.submit(update_debug_info)

        DebugDisplay.draw_text(screenshot, self.debug_text, 10, 500, (0, 255, 0))
        return screenshot

    @staticmethod
    def get_color_mask(screenshot, color):
        screenshot = mask_ui(cv.cvtColor(screenshot, cv.COLOR_BGR2HSV))
        lower_limit, upper_limit = get_color_limits(color)
        mask = cv.inRange(screenshot, lower_limit, upper_limit)
        mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
        return mask

    @staticmethod
    def draw_point(img, x, y, color=(0, 0, 255), thickness=5, label=None):
        cv.rectangle(img, (x - thickness, y - thickness), (x + thickness, y + thickness), color=color,
                     thickness=-1, lineType=cv.LINE_AA)
        if label is not None:
            cv.putText(img, label, (x - thickness, y - thickness - 10), cv.FONT_HERSHEY_SIMPLEX, 1, color,
                       2, cv.LINE_AA)

    @staticmethod
    def draw_text(img, text, x, y, color=(0, 0, 255), thickness=2):
        for text in text.split('\n'):
            cv.putText(img, text, (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, color, thickness, cv.LINE_AA)
            y += 50
