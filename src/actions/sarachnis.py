from src.actions.combat import CombatAction
from src.actions.types.action_status import ActionStatus
from src.robot import robot
from src.robot.timing.timer import Timer
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import Prayer


class SarachnisAction(CombatAction):
    def __init__(self):
        super().__init__(target=Color.RED, health_threshold=70, prayers=[Prayer.PROTECT_FROM_MELEE])

    def first_tick(self):
        self.set_progress_message('Fighting Sarachnis...')

    def tick(self, timing):
        timing.interval(Timer.sec2tick(1), self.reengage_combat)
        combat_status = timing.poll(Timer.sec2tick(0.1), self.poll_combat_status)
        return timing.exit_status(combat_status)

    def reengage_combat(self):
        _, distance = vision.get_contour(vision.grab_screen(), self.target)
        if distance > 500:  # 500 is upper limit for melee range
            robot.click_contour(Color.RED)

    def poll_combat_status(self):
        status = super().tick(self.timing)
        if status.is_terminal():
            return status

    def last_tick(self):
        super().last_tick()
