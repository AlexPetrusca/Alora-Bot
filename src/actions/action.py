import logging
import math
from abc import abstractmethod
from enum import Enum

TICK_INTERVAL = 0.1  # 100ms tick
    

class Action:
    play_count = -1
    tick_counter = -1
    progress_message = ""

    @abstractmethod
    def first_tick(self):
        ...

    @abstractmethod
    def tick(self, t):
        ...

    @abstractmethod
    def last_tick(self):
        ...

    def run(self, t):
        if self.tick_counter == -1:
            self.first_tick()
            self.tick_counter = 0
        if Action.sec2tick(t) >= self.tick_counter:
            status = self.tick(t)
            if status.is_terminal():
                self.last_tick()
                self.tick_counter = -1
                return status
            self.tick_counter += 1
        return Action.Status.IN_PROGRESS

    def set_progress_message(self, progress_message):
        self.progress_message = progress_message
        logging.info(self.progress_message)

    def play(self, count):
        self.play_count = count
        return self

    def play_once(self):
        return self.play(1)

    @staticmethod
    def sec2tick(secs):
        return math.floor(secs / TICK_INTERVAL)

    @staticmethod
    def tick2sec(ticks):
        return ticks * TICK_INTERVAL

    class Status(Enum):
        NOT_STARTED = 1
        IN_PROGRESS = 2
        ABORTED = 3
        COMPLETE = 4

        # def __init__(self):
        #     self._reason = None
        #
        # def reason(self, reason):
        #     self._reason = reason

        def is_terminal(self):
            return self == Action.Status.COMPLETE or self == Action.Status.ABORTED
