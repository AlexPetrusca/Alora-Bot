from src.actions.primitives.action import Action
from src.robot import robot
from src.robot.timing.timer import Timer
from src.vision.coordinates import HealActionCoord, BankMenu
from src.vision.images import Images


class HealAction(Action):
    def __init__(self, bank=False):
        super().__init__()
        self.bank = bank

    def first_tick(self):
        self.set_progress_message("Routing to Healer...")

    def tick(self, timing):
        timing.execute(lambda: robot.shift_click(HealActionCoord.WALK1))  # move to teleport wizard
        timing.execute_after(Timer.sec2tick(4), lambda: robot.click(HealActionCoord.PRAYER_ALTAR))
        timing.execute_after(Timer.sec2tick(8), lambda: robot.right_click(HealActionCoord.HEALER))
        timing.execute_after(Timer.sec2tick(1), lambda: robot.click_image(Images.Menu.HEAL_OPTION, 0.9))
        if self.bank:
            timing.execute_after(Timer.sec2tick(3), lambda: robot.click(HealActionCoord.BANK_CHEST))
            timing.execute_after(Timer.sec2tick(4), lambda: robot.click(BankMenu.CLOSE))
            return timing.complete_after(Timer.sec2tick(1))
        else:
            return timing.complete_after(Timer.sec2tick(1))

    def last_tick(self):
        pass
