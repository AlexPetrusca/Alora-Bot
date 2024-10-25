from src.actions.breadcrumb_trail import BreadcrumbTrailAction
from src.actions.combat.combat import CombatAction
from src.robot import robot
from src.robot.timing.timer import Timer
from src.vision.color import Color
from src.vision.coordinates import Prayer
from src.vision.images import Potion


class VampyreAction(CombatAction):
    def __init__(self):
        super().__init__(potions=[Potion.SUPER_COMBAT], sip_prayer=True)

        self.breadcrumb_action = BreadcrumbTrailAction(Color.YELLOW, target=0)

    def first_tick(self):
        self.set_progress_message('Fighting Vampyres...')

    def respond_to_combat_event(self, timing, prev_event, event):
        if event == CombatAction.Event.SIP_PRAYER:
            timing.execute(lambda: robot.click_contour(Color.GREEN))
            timing.wait(Timer.sec2tick(5))
            timing.action(self.breadcrumb_action)
        else:
            super().respond_to_combat_event(timing, prev_event, event)
