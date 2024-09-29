import logging
from src.actions.action import Action


class WaitAction(Action):
    d = 0

    def __init__(self, d):
        self.d = d

    def first_tick(self):
        self.set_status(f'Waiting {self.d} seconds...')

    def tick(self, t):
        return t > self.d

    def last_tick(self):
        pass
