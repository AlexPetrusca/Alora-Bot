import cv2 as cv
import mss

from src.actions.action import Action
from src.robot import robot
from src.vision import vision
from src.vision.coordinates import ControlPanel, StandardSpellbook


class PickUpItemsAction(Action):
    sct = mss.mss()
    pause_on_fail = True

    item_found = False
    tp_home_tick = None
    click_count = 0
    retry_count = 0

    def __init__(self, pause_on_fail=True):
        self.pause_on_fail = pause_on_fail

    def first_tick(self):
        self.set_status('Picking Up Ground Items...')
        pass

    def tick(self, t):
        if self.tick_counter == 0:
            click_xy = vision.locate_ground_item(vision.grab_screen(self.sct))
            if click_xy is not None:
                self.item_found = True
                robot.click(click_xy[0] / 2, click_xy[1] / 2)
            elif not self.pause_on_fail:
                return True  # exit quickly if item not found and not pausing on failure

        if self.tick_counter > Action.sec2tick(3):
            if self.item_found:
                if self.tick_counter % Action.sec2tick(0.25) == 0 and self.tp_home_tick is None:
                    click_xy = vision.locate_ground_item(vision.grab_screen(self.sct))
                    if click_xy is not None:
                        if vision.read_latest_chat(self.sct).find("You do not have enough inventory space.") == 0:
                            self.tp_home_tick = self.tick_counter
                        robot.click(click_xy[0] / 2, click_xy[1] / 2)
                        self.click_count += 1
                    else:
                        self.retry_count += 1
            else:
                return self.tick_counter > Action.sec2tick(10)  # item not found, pause in case user wants to take action

        if self.tp_home_tick is not None:
            if self.tick_counter == self.tp_home_tick:
                robot.click(ControlPanel.MAGIC_TAB)
            if self.tick_counter == self.tp_home_tick + Action.sec2tick(0.5):
                robot.click(StandardSpellbook.HOME_TELEPORT)
            return self.tick_counter > self.tp_home_tick + Action.sec2tick(5)
        if self.click_count > 20:
            print("Find item failed - excessive click count")
            return True
        if self.retry_count > 4:
            print("Find item stopped - retry timeout")
            return True

        return False

    def last_tick(self):
        self.item_found = False
        self.tp_home_tick = None
        self.click_count = 0
        self.retry_count = 0

    # replace with Status.ABORTED
    def did_tp_home(self):
        return self.tp_home_tick is not None
