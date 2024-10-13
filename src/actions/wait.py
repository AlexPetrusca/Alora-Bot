from src.actions.primitives.action import Action
from src.robot.timing.timer import Timer


class WaitAction(Action):
    def __init__(self, duration):
        super().__init__()
        self.duration = duration

    def first_tick(self):
        self.set_progress_message(f'Waiting {self.duration} seconds...')

    def tick(self, timing):
        return timing.complete_after(Timer.sec2tick(self.duration))

    def last_tick(self):
        pass
