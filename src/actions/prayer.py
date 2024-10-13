from src.actions.primitives.action import Action
from src.robot import robot
from src.robot.timer import Timer
from src.vision.coordinates import ControlPanel


class PrayerAction(Action):
    def __init__(self, *prayers, fast_switch=True, switch_inventory=False):
        super().__init__()
        self.prayers = set(prayers)  # ground truth
        self.active_prayers = set()  # in-game truth
        self.fast_switch = fast_switch
        self.switch_inventory = switch_inventory

    def first_tick(self):
        self.set_progress_message(f'Toggling prayers...')

    def tick(self, timing):
        if self.fast_switch:
            timing.execute(lambda: robot.press('1'))
            self.click_sync_prayers(timing, Timer.sec2tick(0.1))
            if self.switch_inventory:
                timing.execute_after(Timer.sec2tick(0.1), lambda: robot.press('Space'))
        else:
            timing.execute(lambda: robot.click(ControlPanel.PRAYER_TAB))
            self.click_sync_prayers(timing, Timer.sec2tick(0.5))
            if self.switch_inventory:
                timing.execute_after(Timer.sec2tick(0.5), lambda: robot.click(ControlPanel.INVENTORY_TAB))

        return timing.complete()

    def click_sync_prayers(self, timing, tick_duration):
        # enable prayers
        for prayer in self.prayers:
            timing.execute_after(tick_duration, lambda: self.click_enable_prayer(prayer))
        # disable prayers
        removal_set = set()
        for prayer in self.active_prayers:
            timing.execute_after(tick_duration, lambda: self.click_disable_prayer(prayer, removal_set))
        self.active_prayers -= removal_set

    def click_enable_prayer(self, prayer):
        if prayer not in self.active_prayers:
            robot.click(prayer)
            self.active_prayers.add(prayer)

    def click_disable_prayer(self, prayer, removal_set):
        if prayer not in self.prayers:
            robot.click(prayer)
            removal_set.add(prayer)

    def enable_prayer(self, prayer):
        if prayer is not None and prayer not in self.prayers:
            self.prayers.add(prayer)
        return self

    def enable_prayers(self, *prayers):
        for prayer in prayers:
            self.enable_prayer(prayer)
        return self

    def disable_prayer(self, prayer):
        if prayer is not None and prayer in self.prayers:
            self.prayers.remove(prayer)
        return self

    def disable_prayers(self, *prayers):
        for prayer in prayers:
            self.disable_prayer(prayer)
        return self

    def set_prayer(self, prayer):
        self.disable_all_prayers()
        self.enable_prayer(prayer)
        return self

    def set_prayers(self, *prayers):
        self.disable_all_prayers()
        self.enable_prayers(*prayers)
        return self

    def disable_all_prayers(self):
        self.prayers.clear()

    def last_tick(self):
        self.active_prayers = set()
