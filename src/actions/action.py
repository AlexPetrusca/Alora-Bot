import math
from abc import abstractmethod

TICK_INTERVAL = 0.1  # 100ms tick


class Action:
    tick_counter = -1

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
                # print(self.tick_counter)
                self.last_tick()
                self.tick_counter = -1
                return True
            self.tick_counter += 1
        return False

    @staticmethod
    def sec2tick(secs):
        return math.floor(secs / TICK_INTERVAL)

    @staticmethod
    def tick2sec(ticks):
        return ticks * TICK_INTERVAL
