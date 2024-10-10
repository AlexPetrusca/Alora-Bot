from enum import Enum
from time import perf_counter


class Timer:
    TICK_INTERVAL = 0.1  # 100ms tick

    def __init__(self):
        self.tick_counter = 0
        self.t_last = 0
        self.paused = False

    def run(self):
        if not self.paused:
            t = perf_counter()
            if t - self.t_last >= Timer.TICK_INTERVAL:
                self.tick_counter += 1
                self.t_last = t
                return Timer.Status.TICK
            else:
                return Timer.Status.WAITING
        else:
            return Timer.Status.PAUSED

    def pause(self):
        self.paused = True

    def play(self):
        self.paused = False
        self.t_last = perf_counter()

    def reset(self):
        self.tick_counter = 0
        self.t_last = perf_counter()

    @staticmethod
    def sec2tick(secs):
        return secs // Timer.TICK_INTERVAL

    @staticmethod
    def tick2sec(ticks):
        return ticks * Timer.TICK_INTERVAL

    class Status(Enum):
        TICK = 0
        WAITING = 1
        PAUSED = 2
