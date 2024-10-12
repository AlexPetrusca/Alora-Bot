import logging
import math
from abc import abstractmethod
from enum import Enum


class TimingRecord:
    def __init__(self, tick, status):
        self.tick = tick
        self.status = status


class ActionTiming:
    def __init__(self):
        self.tick_counter = -1
        self.tick_offset = 0
        self.start_tick = -1
        self.timing_records = dict()

    def update(self, global_tick):
        if self.start_tick == -1:
            self.start_tick = global_tick
        self.tick_counter = global_tick - self.start_tick
        self.tick_offset = 0

    def reset(self):
        self.tick_counter = -1
        self.tick_offset = 0
        self.start_tick = -1
        self.timing_records.clear()

    def wait(self, tick_duration):
        self.tick_offset += tick_duration
        return self.tick_counter == self.tick_offset

    # todo: should this also latch and return the result of the function?
    def execute(self, fn):
        if not callable(fn):
            raise AssertionError(f"{fn} is not callable")

        if self.tick_counter == self.tick_offset:
            fn()
        return self.tick_counter == self.tick_offset

    def complete(self):
        if self.tick_counter >= self.tick_offset:
            return Action.Status.COMPLETE
        else:
            return Action.Status.IN_PROGRESS

    def abort(self):
        if self.tick_counter >= self.tick_offset:
            return Action.Status.ABORTED
        else:
            return Action.Status.IN_PROGRESS

    def execute_after(self, tick_duration, fn):
        if not callable(fn):
            raise AssertionError(f"{fn} is not callable")

        self.wait(tick_duration)
        return self.execute(fn)

    def complete_after(self, tick_duration):
        self.wait(tick_duration)
        return self.complete()

    def abort_after(self, tick_duration):
        self.wait(tick_duration)
        return self.abort()

    def interval(self, tick_interval, fn, ignore_scheduling=False):
        if not callable(fn):
            raise AssertionError(f"{fn} is not callable")

        # poll_record = self.timing_records.get(fn)
        # if (ignore_scheduling or self.tick_counter >= self.tick_offset) and self.tick_counter % tick_interval == 0:
        #     status = fn()
        #     self.timing_records[fn] = TimingRecord(self.tick_counter, status)
        #     return status
        # elif poll_record is not None:
        #     return poll_record.status
        # else:
        #     return None

        is_scheduled = ignore_scheduling or self.tick_counter >= self.tick_offset
        if is_scheduled and self.tick_counter % tick_interval == 0:
            return fn()
        return None

    # todo: [important] poll doesn't work with lambdas... fn needs to be a fixed address
    def poll(self, tick_interval, fn):
        if not callable(fn):
            raise AssertionError(f"{fn} is not callable")

        poll_record = self.timing_records.get(fn)
        if poll_record is None:
            if self.tick_counter >= self.tick_offset and self.tick_counter % tick_interval == 0:
                status = fn()
                if status is not None:
                    self.timing_records[fn] = TimingRecord(self.tick_counter, status)
                    self.tick_offset = self.tick_counter
                    return status

            self.tick_offset = math.inf
            return None

        self.tick_offset = poll_record.tick
        return poll_record.status

    def action(self, action):
        if self.tick_counter >= self.tick_offset:
            action_record = self.timing_records.get(action)
            if action_record is None:  # in progress?
                status = action.run(self.tick_counter)
                if status.is_terminal():
                    self.timing_records[action] = TimingRecord(self.tick_counter, status)
                    self.tick_offset = self.tick_counter
                else:
                    self.tick_offset = math.inf
                return status
            else:  # completed?
                self.tick_offset = action_record.tick
                return action_record.status
        else:  # not started?
            self.tick_offset = math.inf
            return Action.Status.NOT_STARTED

    def actions(self, *actions):
        for action in actions:
            self.action(action)


class Action:
    def __init__(self):
        self.timing = ActionTiming()
        self.play_count = -1
        self.progress_message = ""

    @abstractmethod
    def first_tick(self):
        ...

    @abstractmethod
    def tick(self, timing: ActionTiming):
        ...

    @abstractmethod
    def last_tick(self):
        ...

    def run(self, global_tick):
        if self.timing.tick_counter == -1:
            self.first_tick()

        self.timing.update(global_tick)
        status = self.tick(self.timing)
        if status.is_terminal():
            self.last_tick()
            self.timing.reset()
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
