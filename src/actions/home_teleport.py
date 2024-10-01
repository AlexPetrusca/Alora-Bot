from src.actions.action import Action
from src.util import robot
from src.vision.coordinates import Interface, StandardSpellbook


class HomeTeleportAction(Action):
    def first_tick(self):
        self.set_status('Teleporting Home...')

    def tick(self, t):
        if self.tick_counter == 0:
            robot.click(Interface.MAGIC_TAB)
        if self.tick_counter == Action.sec2tick(1):
            robot.click(StandardSpellbook.HOME_TELEPORT)
        return self.tick_counter == Action.sec2tick(4)

    def last_tick(self):
        pass
