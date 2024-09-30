import mss
from pytesseract import pytesseract

from src.actions.action import Action
from src.util import robot
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import Controls, StandardSpellbook


class CombatAction(Action):
    sct = mss.mss()
    target_color = Color.RED
    health_threshold = 30

    fight_over_tick = None
    tp_home_tick = None
    retry_count = 0

    def __init__(self, target_color=Color.RED, health_threshold=30):
        self.target_color = target_color
        self.health_threshold = health_threshold

    def first_tick(self):
        pass

    def tick(self, t):
        if self.tick_counter == 0:
            robot.click_contour(self.target_color)
        if self.tick_counter == Action.sec2tick(1):
            robot.click(Controls.INVENTORY_TAB)
        if self.tick_counter > Action.sec2tick(4) and self.fight_over_tick is None:
            if self.tick_counter % Action.sec2tick(1) == 0:
                # check fight end
                damage_ui = vision.grab_damage_ui(mss.mss())
                ocr = pytesseract.image_to_string(damage_ui).strip()
                print('"', ocr, '"', len(ocr))
                if ocr.startswith("0/"):
                    self.fight_over_tick = self.tick_counter
                elif ocr.find("/") == -1:  # "/" not found
                    self.retry_count += 1
                    if self.retry_count >= 3:
                        self.fight_over_tick = self.tick_counter
                # eat food or teleport home on low health
                if vision.read_hitpoints(self.sct) < self.health_threshold:
                    ate_food = robot.click_food()
                    if not ate_food:
                        self.fight_over_tick = self.tick_counter
                        self.tp_home_tick = self.tick_counter

        if self.tp_home_tick is not None:
            if self.tick_counter == self.tp_home_tick:
                robot.click(Controls.MAGIC_TAB)
            if self.tick_counter == self.tp_home_tick + Action.sec2tick(0.5):
                robot.click(StandardSpellbook.HOME_TELEPORT)
            return self.tick_counter > self.tp_home_tick + Action.sec2tick(4)
        elif self.fight_over_tick is not None:
            return self.tick_counter > self.fight_over_tick + Action.sec2tick(4)
        else:
            return False

    def last_tick(self):
        self.fight_over_tick = None
        self.tp_home_tick = None
        self.retry_count = 0

    # replace with Status.ABORTED
    def did_tp_home(self):
        return self.tp_home_tick is not None
