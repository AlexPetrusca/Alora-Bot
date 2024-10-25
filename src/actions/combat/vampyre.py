from src.actions.combat.combat import CombatAction
from src.robot import robot
from src.vision.color import Color
from src.vision.coordinates import Prayer
from src.vision.images import Potion


class VampyreAction(CombatAction):
    def __init__(self):
        super().__init__(
            prayers=[Prayer.PROTECT_FROM_MELEE],
            potions=[Potion.SUPER_COMBAT],
            sip_prayer=True
        )

    def first_tick(self):
        self.set_progress_message('Fighting Vampyres...')

    def respond_to_combat_event(self, timing, prev_event, event):
        if event == CombatAction.Event.SIP_PRAYER:
            timing.execute(lambda: robot.click_contour(Color.GREEN))
        else:
            super().respond_to_combat_event(timing, prev_event, event)


