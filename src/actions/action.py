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

    def play(self, count):
        self.play_count = count
        return self

    def play_once(self):
        return self.play(1)

    def wait(self, tick_duration):
        self.tick_offset += tick_duration
        return self.tick_counter == self.tick_offset

    def execute(self, fn):
        if self.tick_counter == self.tick_offset:
            fn()
        return self.tick_counter == self.tick_offset

    def complete(self):
        if self.tick_counter == self.tick_offset:
            return Action.Status.COMPLETE
        else:
            return Action.Status.IN_PROGRESS

    def abort(self):
        if self.tick_counter == self.tick_offset:
            return Action.Status.COMPLETE
        else:
            return Action.Status.ABORTED

    def execute_after(self, tick_duration, fn):
        self.wait(tick_duration)
        return self.execute(fn)

    def complete_after(self, tick_duration):
        if self.wait(tick_duration):
            return Action.Status.COMPLETE
        else:
            return Action.Status.IN_PROGRESS

    def abort_after(self, tick_duration):
        if self.wait(tick_duration):
            return Action.Status.ABORTED
        else:
            return Action.Status.IN_PROGRESS

    def interval(self, tick_interval, fn):
        if self.tick_counter >= self.tick_offset and self.tick_counter % tick_interval == 0:
            fn()
        return self.tick_counter >= self.tick_offset and self.tick_counter % tick_interval == 0

    def action(self, action):
        if self.tick_counter == self.tick_offset:
            action.tick()

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
