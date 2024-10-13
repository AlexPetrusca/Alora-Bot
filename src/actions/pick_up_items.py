from enum import Enum

from src.actions.primitives.action import Action
from src.actions.types.action_status import ActionStatus
from src.robot import robot
from src.robot.timing.timer import Timer
from src.vision import vision
from src.vision.coordinates import ControlPanel, StandardSpellbook


class PickUpItemsAction(Action):
    def __init__(self):
        super().__init__()
        self.click_count = 0
        self.retry_count = 0

    def first_tick(self):
        self.set_progress_message('Picking Up Ground Items...')

    def tick(self, timing):
        first_item_found = timing.execute(self.pickup_first_item, capture_result=True)
        if not first_item_found:
            return timing.complete()

        timing.wait(Timer.sec2tick(3))
        pickup_status = timing.poll(Timer.sec2tick(0.2), self.pickup_subsequent_items)
        if pickup_status == PickUpItemsAction.Event.INVENTORY_FULL:
            timing.execute(lambda: robot.click(ControlPanel.MAGIC_TAB))
            timing.execute_after(Timer.sec2tick(0.5), lambda: robot.click(StandardSpellbook.HOME_TELEPORT))
            return timing.abort_after(Timer.sec2tick(5))
        elif pickup_status == PickUpItemsAction.Event.CLICK_TIMEOUT:
            print("Find item failed - excessive click count")
            return timing.complete()
        elif pickup_status == PickUpItemsAction.Event.RETRY_TIMEOUT:
            print("Find item stopped - retry timeout")
            return timing.complete()

        return ActionStatus.IN_PROGRESS

    def pickup_first_item(self):
        click_xy = vision.locate_ground_item(vision.grab_screen())
        if click_xy is not None:
            robot.click(click_xy[0] / 2, click_xy[1] / 2)
            return True
        return False

    def pickup_subsequent_items(self):
        click_xy = vision.locate_ground_item(vision.grab_screen())
        if click_xy is not None:
            robot.click(click_xy[0] / 2, click_xy[1] / 2)
            self.click_count += 1
            if vision.read_latest_chat().find("You do not have enough inventory space.") == 0:
                return PickUpItemsAction.Event.INVENTORY_FULL
            elif self.click_count >= 20:
                return PickUpItemsAction.Event.CLICK_TIMEOUT
        else:
            self.retry_count += 1
            if self.retry_count >= 4:
                return PickUpItemsAction.Event.RETRY_TIMEOUT

    def last_tick(self):
        self.click_count = 0
        self.retry_count = 0

    class Event(Enum):
        INVENTORY_FULL = 2
        CLICK_TIMEOUT = 3
        RETRY_TIMEOUT = 4
