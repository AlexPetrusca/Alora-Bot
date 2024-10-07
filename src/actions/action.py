import logging
from abc import abstractmethod
from enum import Enum


class Action:
    play_count = -1
    progress_message = ""

    start_tick = -1
    prev_tick = -1

    @abstractmethod
    def first_tick(self):
        ...

    @abstractmethod
    def tick(self, tick_counter):
        ...

    @abstractmethod
    def last_tick(self):
        ...

    def run(self, tick_counter):
        if self.start_tick == -1:
            self.start_tick = tick_counter
            self.prev_tick = -1
            self.first_tick()
        local_tick_counter = tick_counter - self.start_tick
        if local_tick_counter > self.prev_tick:
            self.prev_tick = local_tick_counter
            status = self.tick(local_tick_counter)
            if status.is_terminal():
                self.last_tick()
                self.start_tick = -1
                return status
        return Action.Status.IN_PROGRESS

    def set_progress_message(self, progress_message):
        self.progress_message = progress_message
        logging.info(self.progress_message)

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
