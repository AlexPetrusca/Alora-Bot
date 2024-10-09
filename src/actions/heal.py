from src.actions.primitives.action import Action
from src.robot import robot
from src.robot.timer import Timer
from src.vision.coordinates import HealActionCoord, BankMenu
from src.vision.images import Images


class HealAction(Action):
    def __init__(self, bank=False):
        super().__init__()
        self.bank = bank

    def first_tick(self):
        self.set_progress_message("Routing to Healer...")

    def tick(self):
        if self.tick_counter == 0:
            robot.shift_click(HealActionCoord.WALK1)  # move to teleport wizard
        if self.tick_counter == Timer.sec2tick(4):
            robot.click(HealActionCoord.PRAYER_ALTAR)  # click prayer altar
        if self.tick_counter == Timer.sec2tick(12):
            robot.right_click(HealActionCoord.HEALER)  # right click healer
        if self.tick_counter == Timer.sec2tick(13):
            robot.click_image(Images.HEAL_OPTION, 0.9)
        if self.bank:
            if self.tick_counter == Timer.sec2tick(16):
                robot.click(HealActionCoord.BANK_CHEST)  # click bank chest
            if self.tick_counter == Timer.sec2tick(20):
                robot.click(BankMenu.CLOSE)  # close bank
            if self.tick_counter == Timer.sec2tick(21):
                return Action.Status.COMPLETE
        else:
            if self.tick_counter == Timer.sec2tick(14):
                return Action.Status.COMPLETE
        return Action.Status.IN_PROGRESS

    def last_tick(self):
        pass
