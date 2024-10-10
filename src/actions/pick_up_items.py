from src.actions.primitives.action import Action
from src.robot import robot
from src.robot.timer import Timer
from src.vision import vision
from src.vision.coordinates import ControlPanel, StandardSpellbook


class PickUpItemsAction(Action):
    def __init__(self):
        super().__init__()

        self.item_found = False
        self.tp_home_tick = None
        self.click_count = 0
        self.retry_count = 0

    def first_tick(self):
        self.set_progress_message('Picking Up Ground Items...')

    def tick(self, timing):
        timing.execute(self.pickup_first_item)

        if self.item_found:
            timing.wait(Timer.sec2tick(3))
            # todo: this pattern isn't very nice - can we improve it? say with a poll() method on timing?
            if self.tp_home_tick is None:
                timing.interval(Timer.sec2tick(0.2), lambda: self.pickup_subsequent_items(timing.tick_counter))
        else:
            return Action.Status.COMPLETE

        if self.tp_home_tick is not None:
            timing.tick_offset = self.tp_home_tick  # todo: any way to make this nicer?
            timing.execute(lambda: robot.click(ControlPanel.MAGIC_TAB))
            timing.execute_after(Timer.sec2tick(0.5), lambda: robot.click(StandardSpellbook.HOME_TELEPORT))
            return timing.abort_after(Timer.sec2tick(5))
        if self.click_count > 20:
            print("Find item failed - excessive click count")
            return Action.Status.COMPLETE
        if self.retry_count > 4:
            print("Find item stopped - retry timeout")
            return Action.Status.COMPLETE

        return Action.Status.IN_PROGRESS

    def pickup_first_item(self):
        click_xy = vision.locate_ground_item(vision.grab_screen())
        if click_xy is not None:
            self.item_found = True
            robot.click(click_xy[0] / 2, click_xy[1] / 2)

    def pickup_subsequent_items(self, tick_counter):
        click_xy = vision.locate_ground_item(vision.grab_screen())
        if click_xy is not None:
            if vision.read_latest_chat().find("You do not have enough inventory space.") == 0:
                self.tp_home_tick = tick_counter
            robot.click(click_xy[0] / 2, click_xy[1] / 2)
            self.click_count += 1
        else:
            self.retry_count += 1

    def last_tick(self):
        self.item_found = False
        self.tp_home_tick = None
        self.click_count = 0
        self.retry_count = 0
