from time import perf_counter

from src.actions.primitives.action import Action
from src.robot import robot
from src.robot.timing.timer import Timer
from src.vision import vision
from src.vision.coordinates import ControlPanel


class PrayerAction(Action):
    def __init__(self, *prayers, fast_switch=True, switch_to_inventory=False):
        super().__init__()
        self.prayers = set(prayers)
        self.fast_switch = fast_switch
        self.switch_inventory = switch_to_inventory

    def first_tick(self):
        pass

    def tick(self, timing):
        def sync_prayers():
            # t0 = perf_counter()
            active_prayers = vision.get_active_prayers()
            # t1 = perf_counter()
            # print("TIMING:", t1 - t0)

            # disable prayers that shouldn't be on
            for prayer in active_prayers:
                if prayer not in self.prayers:
                    robot.click(prayer)

            # enable prayers that should be on
            for prayer in self.prayers:
                if prayer not in active_prayers:
                    robot.click(prayer)

        if self.fast_switch:
            timing.execute(lambda: robot.press('1'))
            timing.execute(sync_prayers)
            if self.switch_inventory:
                timing.execute(lambda: robot.press('Space'))
                # timing.execute_after(Timer.sec2tick(0.1), lambda: robot.press('Space'))
        else:
            timing.execute(lambda: robot.click(ControlPanel.PRAYER_TAB))
            timing.execute(sync_prayers)
            if self.switch_inventory:
                timing.execute_after(Timer.sec2tick(0.5), lambda: robot.click(ControlPanel.INVENTORY_TAB))

        return timing.complete()

    def enable_prayers(self, *prayers):
        self.prayers = self.prayers.union(prayers)

    def disable_prayers(self, *prayers):
        self.prayers = self.prayers.difference(prayers)

    def set_prayers(self, *prayers):
        self.disable_all_prayers()
        self.enable_prayers(*prayers)

    def disable_all_prayers(self):
        self.prayers.clear()

    def last_tick(self):
        pass
