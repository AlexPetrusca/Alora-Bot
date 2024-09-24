import cv2 as cv
import mss

from src.actions.action import Action
from src.util import robot
from src.vision import vision


class PickUpItemsAction(Action):
    sct = mss.mss()

    item_found_tick = None

    def __init__(self):
        pass

    def first_tick(self):
        self.set_status('Picking Up Ground Items...')
        pass

    def tick(self, t):
        if self.tick_counter % Action.sec2tick(10) == 0:
            screenshot = vision.grab_screen(self.sct)
            click_xy = vision.locate_ground_item(screenshot)
            if click_xy is not None:
                self.item_found_tick = self.tick_counter
                robot.click(click_xy[0] / 2, click_xy[1] / 2)
            else:
                # return True  # todo: uncomment
                return self.tick_counter > Action.sec2tick(8)

        if self.item_found_tick is not None:
            # todo: uncomment
            # if self.tick_counter == Action.sec2tick(5):
            #     screenshot = vision.grab_screen(self.sct)
            #     click_xy = vision.locate_ground_item(screenshot)
            #     if click_xy is None:
            #         return True
            if self.tick_counter > self.item_found_tick + Action.sec2tick(5) and self.tick_counter < self.item_found_tick + Action.sec2tick(8):
                if self.tick_counter % Action.sec2tick(0.25) == 0:
                    robot.click(855, 575)

        return False

    def last_tick(self):
        self.item_found_tick = None
