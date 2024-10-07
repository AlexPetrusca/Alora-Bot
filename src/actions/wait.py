import logging
from src.actions.action import Action


class WaitAction(Action):
    d = 0

    def __init__(self, d):
        self.d = d

    def first_tick(self):
        self.set_progress_message(f'Waiting {self.d} seconds...')

    def tick(self, t):
        print("TICK:", t)
        if t > self.d:
            return Action.Status.COMPLETE
        return Action.Status.IN_PROGRESS

    def last_tick(self):
        pass
