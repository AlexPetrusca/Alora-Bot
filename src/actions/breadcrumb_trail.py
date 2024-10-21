import math
from enum import Enum

from src.actions.primitives.action import Action
from src.actions.types.action_status import ActionStatus
from src.robot import robot
from src.robot.timing.timer import Timer
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import Player
from src.vision.images import Images


class BreadcrumbTrailAction(Action):
    CLICK_RETRY_THRESHOLD = 5
    RETRY_THRESHOLD = 3
    DISTANCE_THRESHOLD = 50

    def __init__(self, color=Color.YELLOW, target=-1, disable_auto_retaliate=False):
        super().__init__()
        self.color = color
        self.disable_auto_retaliate = disable_auto_retaliate
        self.target_label = target

        self.found_label = -1
        self.next_label = 0
        self.click_retry_count = 0
        self.retry_count = 0

    def first_tick(self):
        self.set_progress_message(f'Following {self.color.to_string()} breadcrumb trail...')

    def tick(self, timing):
        # if self.disable_auto_retaliate:
        #     timing
        status = timing.poll(Timer.sec2tick(1), self.click_next_breadcrumb)
        if status == BreadcrumbTrailAction.Event.TARGET_REACHED:
            return timing.complete()
        else:
            return timing.abort()

    def click_next_breadcrumb(self):
        breadcrumb_loc, distance = self.find_next_breadcrumb()
        if breadcrumb_loc is not None:
            if self.click_retry_count > BreadcrumbTrailAction.CLICK_RETRY_THRESHOLD:
                print(f"Retrying Click on Breadcrumb {self.found_label}...")
                self.found_label -= 1
                self.click_retry_count = 0
                self.retry_count += 1

            if self.found_label != self.next_label:
                if distance >= BreadcrumbTrailAction.DISTANCE_THRESHOLD:
                    robot.shift_click(breadcrumb_loc)
                self.found_label = self.next_label
            elif distance < BreadcrumbTrailAction.DISTANCE_THRESHOLD:
                self.next_label += 1
                self.click_retry_count = 0
                self.retry_count = 0
            else:
                self.click_retry_count += 1
        else:
            print("Failed finding breadcrumb: ", self.next_label)
            self.retry_count += 1

        if self.target_label > 0 and self.next_label == self.target_label + 1:
            return BreadcrumbTrailAction.Event.TARGET_REACHED
        elif self.retry_count > BreadcrumbTrailAction.RETRY_THRESHOLD:
            return BreadcrumbTrailAction.Event.ABORT

    # todo: this is taking 0.5 seconds - need to speed this up
    def find_next_breadcrumb(self):
        screenshot = vision.grab_screen(hide_ui=True)
        breadcrumb_loc = vision.locate_image(screenshot, Images.YELLOW_MARKERS[self.next_label], 0.8)
        if breadcrumb_loc is not None:
            breadcrumb_loc = breadcrumb_loc[0] / 2, breadcrumb_loc[1] / 2
            distance = math.dist(Player.POSITION.value, breadcrumb_loc)
            return breadcrumb_loc, distance
        else:
            return None, -1

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
        self.next_label = 0
        self.click_retry_count = 0
        self.retry_count = 0

    class Event(Enum):
        ABORT = 0
        TARGET_REACHED = 1
