import mss

from src.actions.primitives.action import Action
from src.robot import robot
from src.robot.timer import Timer
from src.vision import vision
from src.vision.coordinates import ControlPanel, StandardSpellbook


class PickUpItemsAction(Action):
    sct = mss.mss()

    def __init__(self, pause_on_fail=True):
        super().__init__()
        self.pause_on_fail = pause_on_fail

        self.item_found = False
        self.tp_home_tick = None
        self.click_count = 0
        self.retry_count = 0

    def first_tick(self):
        self.set_progress_message('Picking Up Ground Items...')
        pass

    def tick(self):
        if self.tick_counter == 0:
            click_xy = vision.locate_ground_item(vision.grab_screen(self.sct))
            if click_xy is not None:
                self.item_found = True
                robot.click(click_xy[0] / 2, click_xy[1] / 2)
            elif not self.pause_on_fail:
                # todo: should we add a reason message to the status here?
                return Action.Status.COMPLETE  # exit quickly if item not found and not pausing on failure

        if self.tick_counter > Timer.sec2tick(3):
            if self.item_found:
                if self.tick_counter % Timer.sec2tick(0.25) == 0 and self.tp_home_tick is None:
                    click_xy = vision.locate_ground_item(vision.grab_screen(self.sct))
                    if click_xy is not None:
                        if vision.read_latest_chat(self.sct).find("You do not have enough inventory space.") == 0:
                            self.tp_home_tick = self.tick_counter
                        robot.click(click_xy[0] / 2, click_xy[1] / 2)
                        self.click_count += 1
                    else:
                        self.retry_count += 1
            else:
                if self.tick_counter > Timer.sec2tick(10):
                    return Action.Status.COMPLETE  # item not found, pause in case user wants to take action

        if self.tp_home_tick is not None:
            if self.tick_counter == self.tp_home_tick:
                robot.click(ControlPanel.MAGIC_TAB)
            if self.tick_counter == self.tp_home_tick + Timer.sec2tick(0.5):
                robot.click(StandardSpellbook.HOME_TELEPORT)
            if self.tick_counter > self.tp_home_tick + Timer.sec2tick(5):
                return Action.Status.ABORTED
        if self.click_count > 20:
            print("Find item failed - excessive click count")
            return Action.Status.COMPLETE
        if self.retry_count > 4:
            print("Find item stopped - retry timeout")
            return Action.Status.COMPLETE

        return Action.Status.IN_PROGRESS

    def last_tick(self):
        self.item_found = False
        self.tp_home_tick = None
        self.click_count = 0
        self.retry_count = 0
