from enum import Enum

from src.actions.primitives.action import Action
from src.robot import robot
from src.robot.timer import Timer
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import ControlPanel, StandardSpellbook


# todo: [bug] when health bar is halfway, the '/' is dropped by ocr which makes the bot erroneously think combat is over
#   - this happens anywhere where we handle combat this way as well (barrows, cerberus, etc.)
class CombatAction(Action):
    def __init__(self, target=Color.RED, health_threshold=50):
        super().__init__()
        self.target = target
        self.health_threshold = health_threshold

        self.retry_count = 0

    def first_tick(self):
        pass

    def tick(self, timing):
        if self.target is not None:
            timing.execute(lambda: robot.click_contour(self.target))

        timing.execute_after(Timer.sec2tick(1), lambda: robot.click(ControlPanel.INVENTORY_TAB))

        timing.wait(Timer.sec2tick(3))
        combat_status = timing.poll(Timer.sec2tick(1), self.poll_combat)
        if combat_status == CombatAction.Event.FLEE:
            timing.execute(lambda: robot.click(ControlPanel.MAGIC_TAB))
            timing.execute_after(Timer.sec2tick(0.5), lambda: robot.click(StandardSpellbook.HOME_TELEPORT))
            return timing.abort_after(Timer.sec2tick(5))
        elif combat_status == CombatAction.Event.FIGHT_OVER:
            return timing.complete_after(Timer.sec2tick(5))

        return Action.Status.IN_PROGRESS

    def poll_combat(self):
        # check fight end
        ocr = vision.read_damage_ui()
        print('"', ocr, '"', len(ocr))
        if ocr.startswith("0/"):
            return CombatAction.Event.FIGHT_OVER
        elif ocr.find("/") == -1:  # '/' not found
            self.retry_count += 1
            if self.retry_count >= 3:
                return CombatAction.Event.FIGHT_OVER
        else:
            self.retry_count = 0  # '/' found

        # eat food or teleport home on low health
        if vision.read_hitpoints() < self.health_threshold:
            ate_food = robot.click_food()
            if not ate_food:
                return CombatAction.Event.FLEE

        return None

    def last_tick(self):
        self.retry_count = 0

    class Event(Enum):
        FLEE = 1
        FIGHT_OVER = 2
