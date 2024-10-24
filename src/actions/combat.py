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
from src.vision.coordinates import StandardSpellbook, Minimap
from src.vision.images import Potion


# To-do:
#  - Thrall
#  - Status potion


# todo: [bug] when health bar is halfway, the '/' is dropped by ocr which makes the bot erroneously think combat is over
#   - this happens anywhere where we handle combat this way as well (barrows, cerberus, etc.)
class CombatAction(Action):
    RETRY_THRESHOLD = 3

    def __init__(self, target=Color.RED, health_threshold=50, prayer_threshold=20,
                 prayers=None, dodge_hazards=False, flee=True):
        super().__init__()
        self.target = target
        self.health_threshold = health_threshold
        self.prayer_threshold = prayer_threshold
        self.dodge_hazards = dodge_hazards
        self.flee = flee
        self.prayers = prayers if (prayers is not None) else []

        self.poison_retry = 0
        self.combat_retry = 0

        self.prayer_on_action = PrayerAction(*self.prayers)
        self.prayer_off_action = PrayerAction()

    def first_tick(self):
        self.set_progress_message('Fighting...')

    def tick(self, timing):
        if self.target is not None:
            status = timing.poll(Timer.sec2tick(0.5), self.poll_target_visible, play_count=5)
            if status == Timing.PollStatus.ABORTED:
                return timing.complete()
            timing.execute(lambda: robot.click_contour(self.target))

        if len(self.prayers) > 0:
            timing.action(self.prayer_on_action)

        timing.execute_after(Timer.sec2tick(1), lambda: robot.press('Space'))  # inventory tab

        timing.wait(Timer.sec2tick(3))
        if self.dodge_hazards:
            timing.observe(Timer.sec2tick(0.5), self.track_hazards, self.respond_to_hazards)
        combat_status = timing.poll(Timer.sec2tick(1), self.poll_combat_end)

        exit_status = ActionStatus.IN_PROGRESS
        if combat_status == CombatAction.Event.FLEE or combat_status == CombatAction.Event.DEAD:
            exit_status = ActionStatus.ABORTED
            # todo: replace with teleport home action
            timing.execute(lambda: robot.press('2'))  # magic tab
            timing.execute_after(Timer.sec2tick(0.1), lambda: robot.click(StandardSpellbook.HOME_TELEPORT))
        elif combat_status == CombatAction.Event.FIGHT_OVER:
            exit_status = ActionStatus.COMPLETE

        if len(self.prayers) > 0:
            timing.action(self.prayer_off_action)

        return timing.exit_status_after(Timer.sec2tick(5), exit_status)

    def poll_target_visible(self):
        contour = vision.locate_contour(vision.grab_screen(), self.target)
        if contour is not None:
            return True

    def poll_combat_end(self):
        ocr = vision.read_combat_info()
        # print('"', ocr, '"', len(ocr))
        if ocr.startswith("0/"):
            print("COMBAT - FIGHT OVER")
            return CombatAction.Event.FIGHT_OVER
        elif ocr.find("/") == -1:  # '/' not found
            self.combat_retry += 1
            if self.combat_retry >= self.RETRY_THRESHOLD:
                # return CombatAction.Event.DEAD  # todo: this should be returned instead
                print("COMBAT - DIED IN COMBAT")
                return CombatAction.Event.FIGHT_OVER
        else:
            self.combat_retry = 0  # '/' found

        # eat food or teleport home on low health
        if vision.read_hitpoints() < self.health_threshold:
            ate_food = robot.click_food()
            if self.flee and not ate_food:
                print("FLEEING - OUT OF FOOD")
                return CombatAction.Event.FLEE

        # sip prayer potions or teleport home on no prayer
        if vision.read_prayer_energy() < self.prayer_threshold:
            robot.click_potion(Potion.PRAYER)
            # todo: teleport home on no prayer - below doesn't work because we cant read_int below ~25
            if self.flee and vision.read_prayer_energy() == 0:
                print("FLEEING - OUT OF PRAYER")
                return CombatAction.Event.FLEE

        # cure poison or teleport home if unable to
        if vision.is_poisoned():
            if self.flee and self.poison_retry >= self.RETRY_THRESHOLD:
                print("FLEEING - CAN'T CURE POISON")
                return CombatAction.Event.FLEE
            else:
                robot.click(Minimap.HEALTH_ORB)
                self.poison_retry += 1
        else:
            self.poison_retry = 0


    def track_hazards(self):
        hazard = vision.locate_contour(vision.grab_screen(), Color.MAGENTA, area_threshold=100)
        return hazard is not None

    def respond_to_hazards(self, timing, prev_hazard, curr_hazard):
        if not prev_hazard and curr_hazard:
            timing.execute(lambda: robot.click_contour(Color.YELLOW))

    def last_tick(self):
        self.poison_retry = 0
        self.combat_retry = 0

    class Event(Enum):
        DEAD = 0
        FLEE = 1
        FIGHT_OVER = 2
