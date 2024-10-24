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
                 prayers=None, potions=None, eat_food=True, sip_prayer=False,
                 dodge_hazards=False, cure_poison=False, flee=True):
        super().__init__()
        self.target = target
        self.health_threshold = health_threshold
        self.prayer_threshold = prayer_threshold
        self.dodge_hazards = dodge_hazards
        self.eat_food = eat_food
        self.sip_prayer = sip_prayer
        self.cure_poison = cure_poison
        self.flee = flee
        self.prayers = prayers if (prayers is not None) else []
        self.potions = potions if (potions is not None) else []

        self.to_flee = False
        self.food_retry = 0
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

        # todo: is waiting 4 seconds for combat start excessive?
        timing.execute_after(Timer.sec2tick(1), lambda: robot.press('Space'))  # inventory tab
        timing.wait(Timer.sec2tick(3))

        # todo: how do I make sure these don't overlap - ex: need to eat food and sip potion
        if self.dodge_hazards:
            timing.observe(Timer.sec2tick(0.5), self.track_hazards, self.respond_to_combat_event)
        if self.cure_poison:
            timing.observe(Timer.sec2tick(1), self.track_poison, self.respond_to_combat_event)
        if self.sip_prayer:
            timing.observe(Timer.sec2tick(1), self.track_prayer, self.respond_to_combat_event)
        if self.eat_food:
            timing.observe(Timer.sec2tick(1), self.track_hitpoints, self.respond_to_combat_event)
        for potion in self.potions:
            timing.wait(1)
            timing.observe(Timer.sec2tick(5), lambda: self.track_status_potion(potion), self.respond_to_combat_event)
        combat_status = timing.poll(Timer.sec2tick(1), self.poll_combat_over)

        exit_status = ActionStatus.IN_PROGRESS
        if combat_status == CombatAction.Event.FLEE:
            exit_status = ActionStatus.ABORTED
            # todo: replace with teleport home action
            timing.execute(lambda: robot.press('2'))  # magic tab
            timing.execute_after(Timer.sec2tick(0.1), lambda: robot.click(StandardSpellbook.HOME_TELEPORT))
        elif combat_status == CombatAction.Event.FIGHT_OVER:
            exit_status = ActionStatus.COMPLETE

        if len(self.prayers) > 0:
            timing.action(self.prayer_off_action)

        return timing.exit_status_after(Timer.sec2tick(5.5), exit_status)

    def poll_target_visible(self):
        contour = vision.locate_contour(vision.grab_screen(), self.target)
        if contour is not None:
            return True

    def poll_combat_over(self):
        if self.to_flee:
            return CombatAction.Event.FLEE

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

    def respond_to_combat_event(self, timing, prev_event, event):
        if event == CombatAction.Event.EAT_FOOD:
            ate_food = timing.execute(lambda: robot.click_food(), capture_result=True)
            if ate_food is False:
                self.food_retry = self.RETRY_THRESHOLD
            else:
                self.food_retry = 0
        elif event == CombatAction.Event.SIP_PRAYER:
            timing.execute(lambda: robot.click_potion(Potion.PRAYER))
        elif event == CombatAction.Event.CURE_POISON:
            timing.execute(lambda: robot.click(Minimap.HEALTH_ORB))
        elif event == CombatAction.Event.SIP_POTION:
            print("SIP_POTION", event.ctx)
            timing.execute(lambda: robot.click_potion(event.ctx))
        elif event == CombatAction.Event.DODGE_HAZARD:
            timing.execute(lambda: robot.click_contour(Color.YELLOW))
        elif event == CombatAction.Event.FLEE:
            self.to_flee = True

    def track_hitpoints(self):
        # todo: this is potentially broken now - we can flee when we're not out of food
        # eat food or teleport home on low health
        if vision.read_hitpoints() < self.health_threshold:
            if self.flee and self.food_retry >= self.RETRY_THRESHOLD:
                print("FLEEING - OUT OF FOOD")
                return CombatAction.Event.FLEE
            else:
                self.food_retry += 1
                return CombatAction.Event.EAT_FOOD
        else:
            self.food_retry = 0

    def track_prayer(self):
        # sip prayer potions or teleport home on no prayer
        if vision.read_prayer_energy() < self.prayer_threshold:
            if self.flee and vision.read_prayer_energy() == 0:
                print("FLEEING - OUT OF PRAYER")
                return CombatAction.Event.FLEE
            else:
                return CombatAction.Event.SIP_PRAYER

    def track_poison(self):
        # cure poison or teleport home if unable to
        if vision.is_poisoned():
            if self.flee and self.poison_retry >= self.RETRY_THRESHOLD:
                print("FLEEING - CAN'T CURE POISON")
                return CombatAction.Event.FLEE
            else:
                self.poison_retry += 1
                return CombatAction.Event.CURE_POISON
        else:
            self.poison_retry = 0

    def track_status_potion(self, potion):
        if not vision.is_status_active(potion.status):
            return CombatAction.Event.SIP_POTION.with_ctx(potion)

    def track_hazards(self):
        hazard = vision.locate_contour(vision.grab_screen(), Color.MAGENTA, area_threshold=100)
        if hazard is not None:
            return CombatAction.Event.DODGE_HAZARD

    def last_tick(self):
        self.to_flee = False
        self.food_retry = 0
        self.poison_retry = 0
        self.combat_retry = 0

    class Event(Enum):
        DEAD = 0
        FLEE = 1
        FIGHT_OVER = 2

        EAT_FOOD = 3
        SIP_PRAYER = 4
        CURE_POISON = 5
        DODGE_HAZARD = 6
        SIP_POTION = 7

        def __new__(cls, value):
            member = object.__new__(cls)
            member.ctx = None
            return member

        def with_ctx(self, ctx):
            self.ctx = ctx
            return self
