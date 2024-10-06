import cv2 as cv
from src.actions.action import Action
from src.robot import robot
from src.vision.coordinates import HealCoord, ControlPanel


class HealAction(Action):
    bank = False

    def __init__(self, bank=False):
        self.bank = bank

    def first_tick(self):
        self.set_status(f"Routing to Healer... tick={self.tick_counter}")

    def tick(self, t):
        if self.tick_counter == 0:
            robot.shift_click(HealCoord.WALK1)  # move to teleport wizard
        if self.tick_counter == Action.sec2tick(4):
            robot.click(HealCoord.PRAYER_ALTAR)  # click prayer altar
        if self.tick_counter == Action.sec2tick(12):
            robot.right_click(HealCoord.HEALER)  # right click healer
        if self.tick_counter == Action.sec2tick(13):
            robot.click_image(cv.imread('../resources/target/menu/heal_option.png', cv.IMREAD_UNCHANGED), 0.9)
        if self.bank:
            if self.tick_counter == Action.sec2tick(16):
                robot.click(HealCoord.BANK_CHEST)  # click bank chest
            if self.tick_counter == Action.sec2tick(20):
                robot.click(ControlPanel.BANK_CLOSE)  # close bank
            return self.tick_counter == Action.sec2tick(21)
        else:
            return self.tick_counter == Action.sec2tick(14)

    def last_tick(self):
        pass