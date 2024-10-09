from src.actions.primitives.action import Action
from src.robot.timer import Timer


class WaitAction(Action):
    def __init__(self, duration):
        super().__init__()
        self.duration = duration

    def first_tick(self):
        self.set_progress_message(f'Waiting {self.duration} seconds...')

    def tick(self):
        if self.tick_counter > Timer.sec2tick(self.duration):
            return Action.Status.COMPLETE
        return Action.Status.IN_PROGRESS

    def last_tick(self):
        pass
