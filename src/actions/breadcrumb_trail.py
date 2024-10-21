import logging
import math
from enum import Enum
from time import perf_counter

import cv2

from src.actions.auto_retaliate import AutoRetaliateAction
from src.actions.primitives.action import Action
from src.actions.types.action_status import ActionStatus
from src.robot import robot
from src.robot.timing.timer import Timer
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import Player
from src.vision.images import Images
from src.vision.regions import Regions


class BreadcrumbTrailAction(Action):
    CLICK_RETRY_THRESHOLD = 5
    RETRY_THRESHOLD = 3
    EXACT_DISTANCE_THRESHOLD = 25
    CLOSE_DISTANCE_THRESHOLD = 100

    def __init__(self, color=Color.YELLOW, target=-1, dangerous=False):
        super().__init__()
        self.color = color
        self.target_label = target
        self.dangerous = dangerous

        self.found_label = -1
        self.found_loc = None
        self.next_label = 0
        self.click_retry_count = 0
        self.retry_count = 0

        self.auto_retaliate_on_action = AutoRetaliateAction(auto_retaliate=True)
        self.auto_retaliate_off_action = AutoRetaliateAction(auto_retaliate=False)

    def first_tick(self):
        self.set_progress_message(f'Following {self.color.to_string()} breadcrumb trail...')

    def tick(self, timing):
        if self.dangerous:
            timing.action(self.auto_retaliate_off_action)
        _, status = timing.observe(Timer.sec2tick(1), self.click_next_breadcrumb, self.respond)

        if status == BreadcrumbTrailAction.Event.TARGET_REACHED:
            if self.dangerous:
                timing.action(self.auto_retaliate_on_action)
            return timing.complete()
        elif status == BreadcrumbTrailAction.Event.ABORT:
            if self.dangerous:
                timing.action(self.auto_retaliate_on_action)
            return timing.abort()

        return ActionStatus.IN_PROGRESS

    def click_next_breadcrumb(self):
        t0 = perf_counter()
        breadcrumb_loc, modifiers, distance = self.get_next_breadcrumb()
        t1 = perf_counter()
        print("TIMING:", t1 - t0)
        # print('Breadcrumb', self.next_label, '-->', breadcrumb_loc, '|', modifiers, '|', distance)
        if breadcrumb_loc is not None:
            # if self.click_retry_count > BreadcrumbTrailAction.CLICK_RETRY_THRESHOLD:
            #     print(f"Retrying Click on Breadcrumb {self.found_label}...")
            #     self.found_label -= 1
            #     self.click_retry_count = 0
            #     self.retry_count += 1

            if self.found_label != self.next_label:
                self.found_label = self.next_label
                self.found_loc = breadcrumb_loc

            if distance < self.EXACT_DISTANCE_THRESHOLD:
                self.next_label += 1
                # self.click_retry_count = 0
                self.retry_count = 0
            # else:
            #     self.click_retry_count += 1

            if 'W' in modifiers and self.EXACT_DISTANCE_THRESHOLD < distance < self.CLOSE_DISTANCE_THRESHOLD:
                self.found_loc = breadcrumb_loc if (self.found_loc is None) else None  # first loc is imprecise
                return BreadcrumbTrailAction.Event.WEB_BREADCRUMB
            elif 'M' in modifiers and distance < self.CLOSE_DISTANCE_THRESHOLD:
                return BreadcrumbTrailAction.Event.MENU_BREADCRUMB
            elif distance > BreadcrumbTrailAction.EXACT_DISTANCE_THRESHOLD:
                if not self.dangerous or len(modifiers) > 0:
                    return BreadcrumbTrailAction.Event.CLICK_BREADCRUMB
                else:
                    return BreadcrumbTrailAction.Event.SHIFT_CLICK_BREADCRUMB
        else:
            print("Failed finding breadcrumb: ", self.next_label)
            self.retry_count += 1

        if self.target_label > 0 and self.next_label == self.target_label + 1:
            return BreadcrumbTrailAction.Event.TARGET_REACHED
        elif self.retry_count > BreadcrumbTrailAction.RETRY_THRESHOLD:
            return BreadcrumbTrailAction.Event.ABORT

    def respond(self, timing, from_status, to_status):
        timing.execute(lambda: logging.info(f"TO_STATUS --> {to_status}"))
        if to_status == BreadcrumbTrailAction.Event.CLICK_BREADCRUMB:
            timing.execute(lambda: robot.click(self.found_loc))
        elif to_status == BreadcrumbTrailAction.Event.SHIFT_CLICK_BREADCRUMB:
            timing.execute(lambda: robot.shift_click(self.found_loc))
        elif to_status == BreadcrumbTrailAction.Event.WEB_BREADCRUMB:
            for i in range(0, 20):
                timing.execute_after(Timer.sec2tick(0.5), lambda: robot.click(self.found_loc))
                # timing.execute_after(Timer.sec2tick(0.5), lambda: robot.click_contour(self.color))
                # timing.execute_after(Timer.sec2tick(0.5), lambda: robot.click_image(Images.YELLOW_W_MARKER))
        elif to_status == BreadcrumbTrailAction.Event.MENU_BREADCRUMB:
            timing.execute_after(Timer.sec2tick(0.5), lambda: robot.press('1'))


    # todo: this is taking 0.5 seconds - need to speed this up
    def get_next_breadcrumb(self):
        screenshot = vision.grab_screen(hide_ui=True)
        breadcrumb_loc = vision.locate_image(screenshot, Images.YELLOW_MARKERS[self.next_label], 0.75, silent=True)
        if breadcrumb_loc is not None:
            modifiers = self.find_modifiers(screenshot, breadcrumb_loc)
            breadcrumb_loc = breadcrumb_loc[0] // 2, breadcrumb_loc[1] // 2
            distance = math.dist(Player.POSITION.value, breadcrumb_loc)
            return breadcrumb_loc, modifiers, distance
        else:
            return None, None, -1

    def find_modifiers(self, screenshot, loc):
        modifiers = []

        width = 100
        x0 = int(loc[0] - width // 2 if (loc[0] - width // 2 >= 0) else 0)
        y0 = int(loc[1] - width // 2 if (loc[1] - width // 2 >= 0) else 0)
        x1 = int(loc[0] + width // 2 if (loc[0] + width // 2 <= 2 * Regions.SCREEN.w) else 2 * Regions.SCREEN.w)
        y1 = int(loc[1] + width // 2 if (loc[1] + width // 2 <= 2 * Regions.SCREEN.h) else 2 * Regions.SCREEN.h)
        region = screenshot[y0:y1, x0:x1]

        menu_marker_loc = vision.locate_image(region, Images.YELLOW_M_MARKER, 0.75, silent=True)
        if menu_marker_loc is not None:
            modifiers.append('M')
        web_marker_loc = vision.locate_image(region, Images.YELLOW_W_MARKER, 0.75, silent=True)
        if web_marker_loc is not None:
            modifiers.append('W')

        return modifiers

    # def find_next_breadcrumb(self):
    #     screenshot = vision.grab_screen(hide_ui=True)
    #     contour_loc = vision.locate_contour(screenshot, Color.YELLOW, 250)
    #     if contour_loc is not None:
    #         search_width = 100
    #         x0 = contour_loc[0] - search_width // 2 if (contour_loc[0] - search_width // 2 >= 0) else 0
    #         y0 = contour_loc[1] - search_width // 2 if (contour_loc[1] - search_width // 2 >= 0) else 0
    #         x1 = contour_loc[0] + search_width // 2 if (contour_loc[0] + search_width // 2 <= 2 * Regions.SCREEN.w) else 2 * Regions.SCREEN.w
    #         y1 = contour_loc[1] + search_width // 2 if (contour_loc[1] + search_width // 2 <= 2 * Regions.SCREEN.h) else 2 * Regions.SCREEN.h
    #         target_loc = vision.locate_image(screenshot[y0:y1, x0:x1], Images.YELLOW_MARKERS[self.next_label], 0.8, silent=True)
    #         if target_loc is not None:
    #             breadcrumb_loc = (x0 + target_loc[0]) // 2, (y0 + target_loc[1]) // 2
    #             breadcrumb_distance = math.dist(Player.POSITION.value, breadcrumb_loc)
    #             return breadcrumb_loc, breadcrumb_distance
    #
    #     return None, -1

    def last_tick(self):
        self.found_label = -1
        self.found_loc = None
        self.next_label = 0
        self.click_retry_count = 0
        self.retry_count = 0

    class Event(Enum):
        ABORT = 0
        TARGET_REACHED = 1

        CLICK_BREADCRUMB = 2
        SHIFT_CLICK_BREADCRUMB = 3
        WEB_BREADCRUMB = 4
        MENU_BREADCRUMB = 5
