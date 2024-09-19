from src.actions.action import Action
from src.util import robot
from src.util.coordinates import Controls, StandardSpellbook


class HomeTeleportAction(Action):
    def first_tick(self):
        self.set_status('Teleporting Home...')

    def tick(self, t):
        if self.tick_counter == 0:
            robot.click(Controls.MAGIC_TAB.value)
        if self.tick_counter == Action.sec2tick(1):
            robot.click(StandardSpellbook.HOME_TELEPORT.value)
        return self.tick_counter == Action.sec2tick(3)

    def last_tick(self):
        pass
