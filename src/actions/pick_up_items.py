import cv2 as cv
import mss

from src.actions.action import Action
from src.util import robot
from src.vision import vision


class PickUpItemsAction(Action):
    sct = mss.mss()

    item_found = False

    def __init__(self):
        pass

    def first_tick(self):
        self.set_status('Picking Up Ground Items...')
        pass

    def tick(self, t):
        if self.tick_counter == 0:
            click_xy = vision.locate_ground_item(vision.grab_screen(self.sct))
            if click_xy is not None:
                robot.click(click_xy[0] / 2, click_xy[1] / 2)
            else:
                self.item_found = True

        if self.tick_counter > Action.sec2tick(3):
            if self.item_found:
                if self.tick_counter % Action.sec2tick(0.25) == 0:
                    click_xy = vision.locate_ground_item(vision.grab_screen(self.sct))
                    if click_xy is not None:
                        robot.click(click_xy[0] / 2, click_xy[1] / 2)
                    else:
                        return True
            else:
                return True

        return False

    def last_tick(self):
        self.item_found = False
