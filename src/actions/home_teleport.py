from src.actions.primitives.action import Action
from src.robot import robot
from src.robot.timing.timer import Timer
from src.vision.coordinates import ControlPanel, StandardSpellbook


class HomeTeleportAction(Action):
    def first_tick(self):
        self.set_progress_message('Teleporting Home...')

    def tick(self, timing):
        timing.execute(lambda: robot.click(ControlPanel.MAGIC_TAB))
        timing.execute_after(Timer.sec2tick(1), lambda: robot.click(StandardSpellbook.HOME_TELEPORT))
        return timing.complete_after(Timer.sec2tick(3))

    def last_tick(self):
        pass
