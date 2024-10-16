import logging

from src.actions.combat import CombatAction
from src.actions.gear_switch import GearSwitchAction, GearSwitch
from src.actions.prayer import PrayerAction
from src.actions.types.action_status import ActionStatus
from src.robot import robot
from src.robot.timing.timer import Timer
from src.vision import vision
from src.vision.coordinates import Prayer
from src.vision.images import Gear


class DemonicGorillaAction(CombatAction):
    def __init__(self):
        super().__init__(health_threshold=70, flee=False)
        self.last_opp_prayer = None

        self.melee_switch_action = GearSwitchAction(GearSwitch.TWO_BY_THREE, condition_item=Gear.Melee.ARCLIGHT)
        self.ranged_switch_action = GearSwitchAction(GearSwitch.TWO_BY_THREE, condition_item=Gear.Ranged.RUNE_CROSSBOW)

        self.protect_melee_action = PrayerAction(Prayer.PROTECT_FROM_MELEE)
        self.protect_magic_action = PrayerAction(Prayer.PROTECT_FROM_MAGIC)
        self.protect_missiles_action = PrayerAction(Prayer.PROTECT_FROM_MISSILES)

    def first_tick(self):
        self.set_progress_message('Fighting Demonic Gorillas...')

    def tick(self, timing):
        # super().tick(timing)
        timing.observe(Timer.sec2tick(1.0), self.track_opp_prayer, self.respond_to_prayer_change)
        return ActionStatus.IN_PROGRESS

    def respond_to_prayer_change(self, timing, from_status, to_status):
        timing.execute(lambda: logging.info(f"{from_status} --> {to_status}"))
        if to_status == Prayer.PROTECT_FROM_MELEE:
            timing.action(self.protect_missiles_action)
            timing.action(self.ranged_switch_action)
        elif to_status == Prayer.PROTECT_FROM_MAGIC:
            timing.action(self.protect_magic_action)
            timing.action(self.melee_switch_action)
        elif to_status == Prayer.PROTECT_FROM_MISSILES:
            timing.action(self.protect_melee_action)
            timing.action(self.melee_switch_action)

    def track_opp_prayer(self):
        opp_prayer = vision.get_opponent_prayer_protect()
        if opp_prayer is not None:
            self.last_opp_prayer = opp_prayer
        return self.last_opp_prayer

    def last_tick(self):
        self.last_opp_prayer = None
