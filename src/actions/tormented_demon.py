import logging

from src.actions.combat import CombatAction
from src.actions.gear_switch import GearSwitchAction, GearSwitch
from src.actions.types.action_status import ActionStatus
from src.robot import robot
from src.robot.timing.timer import Timer
from src.vision import vision
from src.vision.coordinates import ControlPanel
from src.vision.images import Gear


class TormentedDemonAction(CombatAction):
    def __init__(self):
        super().__init__(health_threshold=70, dodge_hazards=True, flee=False)
        self.last_opp_prayer = None

        self.melee_switch_action = GearSwitchAction(GearSwitch.TWO_BY_THREE, condition_item=Gear.Melee.ARCLIGHT)
        self.magic_switch_action = GearSwitchAction(GearSwitch.TWO_BY_THREE, condition_item=Gear.Magic.TRIDENT_OF_THE_SWAMP)

    def first_tick(self):
        self.set_progress_message('Fighting Tormented Demons...')

    def tick(self, timing):
        super().tick(timing)
        timing.observe(Timer.sec2tick(1.0), self.track_opp_prayer, self.respond_to_prayer_change)
        return ActionStatus.IN_PROGRESS

    def respond_to_hazards(self, timing, prev_hazard, curr_hazard):
        super().respond_to_hazards(timing, prev_hazard, curr_hazard)
        timing.execute(lambda: robot.press('1'))

    def respond_to_prayer_change(self, timing, from_status, to_status):
        timing.execute(lambda: logging.info(f"{from_status} --> {to_status}"))
        if timing.action(self.melee_switch_action) == ActionStatus.COMPLETE:
            return True
        if timing.action(self.magic_switch_action) == ActionStatus.COMPLETE:
            return True
        return False

    def track_opp_prayer(self):
        opp_prayer = vision.get_opponent_prayer_protect()
        if opp_prayer is not None:
            self.last_opp_prayer = opp_prayer
        return self.last_opp_prayer

    def last_tick(self):
        self.last_opp_prayer = None
