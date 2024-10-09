from src.actions.primitives.action import Action
from src.robot import robot
from src.robot.timer import Timer
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import ControlPanel, StandardSpellbook


# todo: [bug] when health bar is halfway, the '/' is dropped by ocr which makes the bot erroneously think combat is over
#   - this happens anywhere where we handle combat this way as well (barrows, cerberus, etc.)
class CombatAction(Action):
    def __init__(self, target=Color.RED, health_threshold=30):
        super().__init__()
        self.target = target
        self.health_threshold = health_threshold

        self.fight_over_tick = None
        self.tp_home_tick = None
        self.retry_count = 0

    def first_tick(self):
        pass

    def tick(self):
        if self.tick_counter == 0 and self.target is not None:
            robot.click_contour(self.target)
        if self.tick_counter == Timer.sec2tick(1):
            robot.click(ControlPanel.INVENTORY_TAB)
        if self.tick_counter > Timer.sec2tick(4) and self.fight_over_tick is None:
            if self.tick_counter % Timer.sec2tick(1) == 0:
                # check fight end
                ocr = vision.read_damage_ui()
                print('"', ocr, '"', len(ocr))
                if ocr.startswith("0/"):
                    self.fight_over_tick = self.tick_counter
                elif ocr.find("/") == -1:  # '/' not found
                    self.retry_count += 1
                    if self.retry_count >= 3:
                        self.fight_over_tick = self.tick_counter
                else:
                    self.retry_count = 0  # '/' found
                # eat food or teleport home on low health
                if vision.read_hitpoints() < self.health_threshold:
                    ate_food = robot.click_food()
                    if not ate_food:
                        self.fight_over_tick = self.tick_counter
                        self.tp_home_tick = self.tick_counter

        if self.tp_home_tick is not None:
            if self.tick_counter == self.tp_home_tick:
                robot.click(ControlPanel.MAGIC_TAB)
            if self.tick_counter == self.tp_home_tick + Timer.sec2tick(0.5):
                robot.click(StandardSpellbook.HOME_TELEPORT)
            if self.tick_counter > self.tp_home_tick + Timer.sec2tick(5):
                return Action.Status.ABORTED
        elif self.fight_over_tick is not None:
            if self.tick_counter > self.fight_over_tick + Timer.sec2tick(5):
                return Action.Status.COMPLETE
        return Action.Status.IN_PROGRESS

    def last_tick(self):
        self.fight_over_tick = None
        self.tp_home_tick = None
        self.retry_count = 0
