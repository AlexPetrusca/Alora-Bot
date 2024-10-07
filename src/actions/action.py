import logging
from abc import abstractmethod
from enum import Enum


class Action:
    play_count = -1
    progress_message = ""

    tick_counter = 0
    tick_offset = 0
    start_tick = -1
    prev_tick = -1

    @abstractmethod
    def first_tick(self):
        ...

    @abstractmethod
    def tick(self):
        ...

    @abstractmethod
    def last_tick(self):
        ...

    def run(self, global_tick):
        if self.start_tick == -1:
            self.start_tick = global_tick
            self.prev_tick = -1
            self.first_tick()

        self.tick_counter = global_tick - self.start_tick
        if self.tick_counter > self.prev_tick:
            self.prev_tick = self.tick_counter
            self.tick_offset = 0
            status = self.tick()
            if status.is_terminal():
                self.last_tick()
                self.start_tick = -1
                return status

        return Action.Status.IN_PROGRESS

    def set_progress_message(self, progress_message):
        self.progress_message = progress_message
        logging.info(self.progress_message)

    def at(self, tick, fn):
        if self.tick_counter == tick:
            fn()

    def after(self, tick_duration, fn):
        self.tick_offset += tick_duration
        self.at(self.tick_offset, fn)

    def interval(self, tick_interval, fn):
        if self.tick_counter % tick_interval == 0:
            fn()

    def play(self, count):
        self.play_count = count
        return self

    def play_once(self):
        return self.play(1)

    class Status(Enum):
        NOT_STARTED = 1
        IN_PROGRESS = 2
        ABORTED = 3
        COMPLETE = 4

        # def __init__(self):
        #     self._reason = None

        # def reason(self, reason):
        #     self._reason = reason

        def is_terminal(self):
            return self == Action.Status.COMPLETE or self == Action.Status.ABORTED
