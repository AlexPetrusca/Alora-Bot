from src.actions.primitives.action import Action
from src.robot.timer import Timer


class WaitAction(Action):
    d = 0

    def __init__(self, d):
        self.d = d

    def first_tick(self):
        self.set_progress_message(f'Waiting {self.d} seconds...')

    def tick(self):
        if self.tick_counter > Timer.sec2tick(self.d):
            return Action.Status.COMPLETE
        return Action.Status.IN_PROGRESS

    def last_tick(self):
        pass
