from src.actions.combat.combat import CombatAction
from src.robot import robot
from src.robot.timing.timer import Timer
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import Prayer


class SarachnisAction(CombatAction):
    DISTANCE_THRESHOLD = 500  # upper limit for melee range

    def __init__(self):
        super().__init__(target=Color.RED, health_threshold=70, prayers=[Prayer.PROTECT_FROM_MELEE])

    def first_tick(self):
        self.set_progress_message('Fighting Sarachnis...')

    def tick(self, timing):
        timing.interval(Timer.sec2tick(1), self.reengage_combat)
        return super().tick(timing)

    def reengage_combat(self):
        _, distance = vision.get_contour(vision.grab_screen(), self.target)
        if distance > self.DISTANCE_THRESHOLD:
            robot.click_contour(Color.RED)

    def last_tick(self):
        super().last_tick()
