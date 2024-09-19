from src.actions.action import Action
from src.util import robot


class HealAction(Action):
    def first_tick(self):
        self.set_status("Routing to Healer...")

    def tick(self, t):
        if self.tick_counter == 0:
            robot.shift_click(700, 302)  # move to teleport wizard
        if self.tick_counter == Action.sec2tick(4):
            robot.click(1292, 68)  # click prayer altar
        if self.tick_counter == Action.sec2tick(10):
            robot.click(1292, 68)  # click prayer altar
        if self.tick_counter == Action.sec2tick(12):
            robot.right_click(805, 520)  # right click healer
        if self.tick_counter == Action.sec2tick(13):
            robot.click(730, 568)  # heal
        return self.tick_counter == Action.sec2tick(14)

    def last_tick(self):
        pass