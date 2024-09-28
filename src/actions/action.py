import logging
import math
from abc import abstractmethod

TICK_INTERVAL = 0.1  # 100ms tick


class Action:
    play_count = -1
    tick_counter = -1
    status = ""

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
            if self.tick(t):
                self.last_tick()
                self.tick_counter = -1
                return True
            self.tick_counter += 1
        return False

    def set_status(self, status):
        self.status = status
        logging.info(self.status)

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
