import mss

from src.actions.action import Action
from src.robot import robot
from src.robot.timer import Timer
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import ControlPanel, StandardSpellbook


# todo: [bug] when health bar is halfway, the '/' is dropped by ocr which makes the bot erroneously think combat is over
#   - this happens anywhere where we handle combat this way as well (barrows, cerberus, etc.)
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

    def tick(self, tick_counter):
        if tick_counter == 0:
            robot.click_contour(self.target_color)
        if tick_counter == Timer.sec2tick(1):
            robot.click(ControlPanel.INVENTORY_TAB)
        if tick_counter > Timer.sec2tick(4) and self.fight_over_tick is None:
            if tick_counter % Timer.sec2tick(1) == 0:
                # check fight end
                ocr = vision.read_damage_ui(mss.mss())
                print('"', ocr, '"', len(ocr))
                if ocr.startswith("0/"):
                    self.fight_over_tick = tick_counter
                elif ocr.find("/") == -1:  # '/' not found
                    self.retry_count += 1
                    if self.retry_count >= 3:
                        self.fight_over_tick = tick_counter
                else:
                    self.retry_count = 0  # '/' found
                # eat food or teleport home on low health
                if vision.read_hitpoints(self.sct) < self.health_threshold:
                    ate_food = robot.click_food()
                    if not ate_food:
                        self.fight_over_tick = tick_counter
                        self.tp_home_tick = tick_counter

        if self.tp_home_tick is not None:
            if tick_counter == self.tp_home_tick:
                robot.click(ControlPanel.MAGIC_TAB)
            if tick_counter == self.tp_home_tick + Timer.sec2tick(0.5):
                robot.click(StandardSpellbook.HOME_TELEPORT)
            if tick_counter > self.tp_home_tick + Timer.sec2tick(5):
                return Action.Status.ABORTED
        elif self.fight_over_tick is not None:
            if tick_counter > self.fight_over_tick + Timer.sec2tick(5):
                return Action.Status.COMPLETE
        return Action.Status.IN_PROGRESS

    def last_tick(self):
        self.fight_over_tick = None
        self.tp_home_tick = None
        self.retry_count = 0
