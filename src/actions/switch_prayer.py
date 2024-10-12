from src.actions.primitives.action import Action
from src.robot import robot
from src.robot.timer import Timer
from src.vision.coordinates import ControlPanel


class SwitchPrayerAction(Action):
    def __init__(self, prayers, fast_switch=True):
        super().__init__()
        self.prayers = prayers
        self.fast_switch = fast_switch

    def first_tick(self):
        self.set_progress_message(f'Toggling prayers...')

    def tick(self, timing):
        if self.fast_switch:
            timing.execute(lambda: robot.press('1'))  # prayer tab
            for prayer in self.prayers:
                timing.execute_after(Timer.sec2tick(0.1), prayer)
            timing.execute_after(Timer.sec2tick(0.1), lambda: robot.press('space'))  # inventory tab
        else:
            timing.execute(lambda: robot.click(ControlPanel.PRAYER_TAB))  # prayer tab
            for prayer in self.prayers:
                timing.execute_after(Timer.sec2tick(0.5), prayer)
            timing.execute_after(Timer.sec2tick(0.5), lambda: robot.click(ControlPanel.INVENTORY_TAB))  # inventory tab

        return timing.complete()

    def last_tick(self):
        pass
