import logging

from src.actions.combat import CombatAction
from src.actions.gear_switch import GearSwitchAction, GearSwitch
from src.actions.prayer import PrayerAction
from src.robot.timing.timer import Timer
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import Prayer
from src.vision.images import Gear


class DemonicGorillaAction(CombatAction):
    def __init__(self):
        super().__init__(target=None, health_threshold=70)
        self.last_protect_prayer_action = None

        self.melee_switch_action = GearSwitchAction(GearSwitch.TWO_BY_THREE, condition_item=Gear.Melee.ARCLIGHT)
        self.ranged_switch_action = GearSwitchAction(GearSwitch.TWO_BY_THREE, condition_item=Gear.Ranged.ARMADYL_CROSSBOW)

        self.protect_melee_action = PrayerAction(Prayer.PROTECT_FROM_MELEE, switch_to_inventory=True)
        self.protect_magic_action = PrayerAction(Prayer.PROTECT_FROM_MAGIC, switch_to_inventory=True)
        self.protect_missiles_action = PrayerAction(Prayer.PROTECT_FROM_MISSILES, switch_to_inventory=True)

    def first_tick(self):
        self.set_progress_message('Fighting Demonic Gorillas...')

    def tick(self, timing):
        timing.observe(Timer.sec2tick(1), self.track_opp_prayer, self.respond_to_prayer_change)

        combat_status = super().tick(timing)

        timing.action(self.melee_switch_action)
        if self.last_protect_prayer_action is not None:
            timing.action(self.last_protect_prayer_action)

        return timing.exit_status(combat_status)

    def respond_to_prayer_change(self, timing, from_status, to_status):
        timing.execute(lambda: logging.info(f"{from_status} --> {to_status}"))
        if to_status == Prayer.PROTECT_FROM_MELEE:
            timing.action(self.protect_missiles_action)
            timing.action(self.ranged_switch_action)
            self.last_protect_prayer_action = self.protect_missiles_action
        elif to_status == Prayer.PROTECT_FROM_MAGIC:
            timing.action(self.protect_magic_action)
            timing.action(self.melee_switch_action)
            self.last_protect_prayer_action = self.protect_magic_action
        elif to_status == Prayer.PROTECT_FROM_MISSILES:
            timing.action(self.protect_melee_action)
            timing.action(self.melee_switch_action)
            self.last_protect_prayer_action = self.protect_melee_action

    def track_opp_prayer(self):
        screenshot = vision.grab_screen()
        red_contour, red_dist = vision.get_contour(screenshot, Color.RED)
        green_contour, green_dist = vision.get_contour(screenshot, Color.GREEN)
        blue_contour, blue_dist = vision.get_contour(screenshot, Color.BLUE)

        closest_dist = 1e10
        prayer = None
        self.target = None
        if red_contour is not None and red_dist < closest_dist:
            closest_dist = red_dist
            prayer = Prayer.PROTECT_FROM_MISSILES
            self.target = Color.RED
        if green_contour is not None and green_dist < closest_dist:
            closest_dist = green_dist
            prayer = Prayer.PROTECT_FROM_MELEE
            self.target = Color.GREEN
        if blue_contour is not None and blue_dist < closest_dist:
            prayer = Prayer.PROTECT_FROM_MAGIC
            self.target = Color.BLUE
        # print(red_dist, green_dist, blue_dist, '-->', self.target)
        return prayer

    def last_tick(self):
        super().last_tick()
        self.target = None
        self.last_protect_prayer_action = None
