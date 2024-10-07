from src.actions.action import Action
from src.robot import robot
from src.robot.timer import Timer
from src.vision.coordinates import ControlPanel, StandardSpellbook


class HomeTeleportAction(Action):
    def first_tick(self):
        self.set_progress_message('Teleporting Home...')

    def tick(self, tick_counter):
        if tick_counter == 0:
            robot.click(ControlPanel.MAGIC_TAB)
        if tick_counter == Timer.sec2tick(1):
            robot.click(StandardSpellbook.HOME_TELEPORT)
        if tick_counter == Timer.sec2tick(4):
            return Action.Status.COMPLETE
        return Action.Status.IN_PROGRESS

    def last_tick(self):
        pass
