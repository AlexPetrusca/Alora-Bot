from copy import copy

from src.actions.primitives.action import Action
from src.robot import robot
from src.robot.timer import Timer
from src.vision.coordinates import ControlPanel


class PrayerAction(Action):
    def __init__(self, prayers=None, fast_switch=True):
        super().__init__()
        self.prayers = set(prayers) if (prayers is not None) else set()  # ground truth
        self.active_prayers = set(prayers) if (prayers is not None) else set()  # in-game truth
        self.fast_switch = fast_switch

    def first_tick(self):
        self.set_progress_message(f'Toggling prayers...')

    def tick(self, timing):
        if self.prayers == self.active_prayers:
            return timing.complete()

        if self.fast_switch:
            timing.execute(lambda: robot.press('1'))  # prayer tab
            self.sync_prayers(timing, Timer.sec2tick(0.1))
            timing.execute_after(Timer.sec2tick(0.1), lambda: robot.press('space'))  # inventory tab
        else:
            timing.execute(lambda: robot.click(ControlPanel.PRAYER_TAB))  # prayer tab
            self.sync_prayers(timing, Timer.sec2tick(0.5))
            timing.execute_after(Timer.sec2tick(0.5), lambda: robot.click(ControlPanel.INVENTORY_TAB))  # inventory tab

        return timing.complete()

    def sync_prayers(self, timing, tick_duration):
        # enable prayers
        for prayer in self.prayers:
            if prayer not in self.active_prayers:
                timing.wait(tick_duration)
                timing.execute(lambda: robot.click(prayer))
                timing.execute(lambda: self.active_prayers.add(prayer))
        # disable prayers
        removal_set = set()
        for prayer in self.active_prayers:
            if prayer not in self.prayers:
                timing.wait(tick_duration)
                timing.execute(lambda: robot.click(prayer))
                timing.execute(lambda: removal_set.add(prayer))
        self.active_prayers -= removal_set

    def enable_prayer(self, prayer):
        if prayer is not None and prayer not in self.prayers:
            self.prayers.add(prayer)
        return self

    def enable_prayers(self, prayers):
        for prayer in prayers:
            self.enable_prayer(prayer)
        return self

    def disable_prayer(self, prayer):
        if prayer is not None and prayer in self.prayers:
            self.prayers.remove(prayer)
        return self

    def disable_prayers(self, prayers):
        for prayer in prayers:
            self.disable_prayer(prayer)
        return self

    def set_prayer(self, prayer):
        self.disable_all_prayers()
        self.enable_prayer(prayer)
        return self

    def set_prayers(self, prayers):
        self.disable_all_prayers()
        self.enable_prayers(prayers)
        return self

    def disable_all_prayers(self):
        self.prayers.clear()
        return self

    def last_tick(self):
        pass
