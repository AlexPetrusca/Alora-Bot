import logging
from enum import Enum

from src.actions.prayer import PrayerAction
from src.actions.primitives.action import Action
from src.actions.types.action_status import ActionStatus
from src.robot import robot
from src.robot.timing.timer import Timer
from src.robot.timing.timing import Timing
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import ControlPanel, StandardSpellbook


# todo: [bug] when health bar is halfway, the '/' is dropped by ocr which makes the bot erroneously think combat is over
#   - this happens anywhere where we handle combat this way as well (barrows, cerberus, etc.)
class CombatAction(Action):
    def __init__(self, target=Color.RED, health_threshold=50, prayers=None, dodge_hazards=False, flee=True):
        super().__init__()
        self.target = target
        self.health_threshold = health_threshold
        self.dodge_hazards = dodge_hazards
        self.flee = flee
        self.prayers = prayers if (prayers is not None) else []

        self.prayer_action = PrayerAction(*self.prayers)
        self.retry_count = 0

    def first_tick(self):
        self.set_progress_message('Fighting...')

    def tick(self, timing):
        if self.target is not None:
            status = timing.poll(Timer.sec2tick(0.5), self.poll_target_visible, play_count=5)
            if status == Timing.PollStatus.ABORTED:
                return timing.complete()
            timing.execute(lambda: robot.click_contour(self.target))

        if len(self.prayers) > 0:
            timing.action(self.prayer_action)

        timing.execute_after(Timer.sec2tick(1), lambda: robot.click(ControlPanel.INVENTORY_TAB))

        timing.wait(Timer.sec2tick(3))
        if self.dodge_hazards:
            timing.observe(Timer.sec2tick(0.5), self.track_hazards, self.respond_to_hazards)
        combat_status = timing.poll(Timer.sec2tick(1), self.poll_combat)

        exit_status = ActionStatus.IN_PROGRESS
        if combat_status == CombatAction.Event.FLEE or combat_status == CombatAction.Event.DEAD:
            exit_status = ActionStatus.ABORTED
            timing.execute(lambda: robot.click(ControlPanel.MAGIC_TAB))
            timing.execute_after(Timer.sec2tick(0.5), lambda: robot.click(StandardSpellbook.HOME_TELEPORT))
        elif combat_status == CombatAction.Event.FIGHT_OVER:
            exit_status = ActionStatus.COMPLETE

        if len(self.prayers) > 0:
            # todo: get rid of if statement; allow prayer action to pass through when prayers is empty or None
            timing.action(self.prayer_action)

        return timing.exit_status_after(Timer.sec2tick(5), exit_status)

    def poll_target_visible(self):
        contour = vision.locate_contour(vision.grab_screen(), self.target)
        if contour is not None:
            return True

    def poll_combat(self):
        # check fight end
        ocr = vision.read_combat_info()
        # print('"', ocr, '"', len(ocr))
        if ocr.startswith("0/"):
            print("COMBAT - FIGHT OVER")
            return CombatAction.Event.FIGHT_OVER
        elif ocr.find("/") == -1:  # '/' not found
            self.retry_count += 1
            if self.retry_count >= 3:
                # return CombatAction.Event.DEAD  # todo: this should be returned instead
                print("COMBAT - DIED IN COMBAT")
                return CombatAction.Event.FIGHT_OVER
        else:
            self.retry_count = 0  # '/' found

        # eat food or teleport home on low health
        if vision.read_hitpoints() < self.health_threshold:
            ate_food = robot.click_food()
            if self.flee and not ate_food:
                print("COMBAT - OUT OF FOOD")
                return CombatAction.Event.FLEE

    def last_tick(self):
        self.retry_count = 0

    def track_hazards(self):
        hazard = vision.locate_contour(vision.grab_screen(), Color.MAGENTA, area_threshold=100)
        return hazard is not None

    def respond_to_hazards(self, timing, prev_hazard, curr_hazard):
        if not prev_hazard and curr_hazard:
            timing.execute(lambda: robot.click_contour(Color.YELLOW))

    class Event(Enum):
        DEAD = 0
        FLEE = 1
        FIGHT_OVER = 2
