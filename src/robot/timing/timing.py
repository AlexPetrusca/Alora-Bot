import math
import inspect
import traceback as tb
from enum import Enum

from src.actions.types.action_status import ActionStatus
from src.robot.timing.timing_record import TimingRecord


class Timing:
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
        if not tick_duration.is_integer():
            raise AssertionError(f"{tick_duration} is not an integer")

        self.tick_offset += tick_duration
        return self.tick_counter == self.tick_offset

    def execute(self, fn, capture_result=False):
        if not callable(fn):
            raise AssertionError(f"{fn} is not callable")

        key = Timing.get_caller_identifier()

        if self.tick_counter == self.tick_offset:
            status = fn()
            if capture_result:
                self.timing_records[key] = TimingRecord(self.tick_counter, status)

        if capture_result:
            execute_record = self.timing_records.get(key)
            if execute_record is None:
                self.block()
                return None
            else:
                self.tick_offset = execute_record.tick
                return execute_record.status
        else:
            return self.tick_counter == self.tick_offset

    def execute_after(self, tick_duration, fn, capture_result=False):
        self.wait(tick_duration)
        return self.execute(fn, capture_result)

    def exit_status(self, action_status):
        if self.tick_counter >= self.tick_offset:
            return action_status
        else:
            return ActionStatus.IN_PROGRESS

    def exit_status_after(self, tick_duration, action_status):
        self.wait(tick_duration)
        return self.exit_status(action_status)

    def complete(self):
        return self.exit_status(ActionStatus.COMPLETE)

    def complete_after(self, tick_duration):
        self.wait(tick_duration)
        return self.complete()

    def abort(self):
        return self.exit_status(ActionStatus.ABORTED)

    def abort_after(self, tick_duration):
        self.wait(tick_duration)
        return self.abort()

    def interval(self, tick_interval, fn, ignore_scheduling=False, play_count=-1):
        if not callable(fn):
            raise AssertionError(f"{fn} is not callable")

        key = Timing.get_caller_identifier()

        # reset latch on first tick
        if self.tick_counter == self.tick_offset:
            action_record = self.timing_records.get(key)
            if action_record is not None:
                self.timing_records.pop(key)

        # process interval on subsequent ticks
        interval_record = self.timing_records.get(key)
        is_scheduled = ignore_scheduling or self.tick_counter >= self.tick_offset
        is_playable = play_count == -1 or interval_record is None or interval_record.play_count > 0
        if is_playable and is_scheduled and self.tick_counter % tick_interval == 0:
            status = fn()
            play_count = interval_record.play_count if (interval_record is not None) else play_count
            new_play_count = play_count - 1 if (play_count != -1) else -1
            self.timing_records[key] = TimingRecord(self.tick_counter, status, play_count=new_play_count)
            return status  # current interval value
        elif interval_record is not None:
            return interval_record.status  # last interval value
        else:
            return None  # interval not called yet

    def observe(self, tick_interval, fn, cb, starting_status=None):
        if not callable(fn):
            raise AssertionError(f"{fn} is not callable")

        def run_cb(timing, from_status, to_status, triggered_tick):
            tick_offset_restore = self.tick_offset
            self.tick_offset = triggered_tick

            param_count = len(inspect.signature(cb).parameters)
            if param_count == 3:
                cb(timing, from_status, to_status)
            elif param_count == 1:
                cb(timing)
            else:
                cb()

            self.tick_offset = tick_offset_restore

        key = Timing.get_caller_identifier()

        prev_record = self.timing_records.get(key)
        if self.tick_counter >= self.tick_offset and self.tick_counter % tick_interval == 0:
            status = fn()
            prev_status = prev_record.status if (prev_record is not None) else starting_status
            if status != prev_status:  # change observed?
                self.timing_records[key] = TimingRecord(self.tick_counter, status, prev_status)
                run_cb(self, prev_status, status, self.tick_counter)
                return prev_status, status

        if prev_record is not None:  # no change observed?
            run_cb(self, prev_record.prev_status, prev_record.status, prev_record.tick)
            return prev_record.prev_status, prev_record.status
        else:  # no value observed?
            return starting_status, starting_status

    def poll(self, tick_interval, fn, default_status=None, play_count=-1):
        if not callable(fn):
            raise AssertionError(f"{fn} is not callable")

        key = Timing.get_caller_identifier()

        # reset latch on first tick
        if self.tick_counter == self.tick_offset:
            action_record = self.timing_records.get(key)
            if action_record is not None:
                self.timing_records.pop(key)

        # process poll on subsequent ticks
        poll_record = self.timing_records.get(key)
        if poll_record is None or poll_record.status is default_status:
            is_playable = play_count == -1 or poll_record is None or poll_record.play_count > 0
            if not is_playable:
                return Timing.PollStatus.ABORTED

            if self.tick_counter >= self.tick_offset and self.tick_counter % tick_interval == 0:
                status = fn()
                play_count = poll_record.play_count if (poll_record is not None) else play_count
                new_play_count = play_count - 1 if (play_count != -1) else -1
                self.timing_records[key] = TimingRecord(self.tick_counter, status, play_count=new_play_count)
                if status is not default_status:
                    self.timing_records[key] = TimingRecord(self.tick_counter, status)
                    self.tick_offset = self.tick_counter
                    return status  # event found

            self.block()
            return None  # event not found

        self.tick_offset = poll_record.tick
        return poll_record.status  # event previously found

    def action(self, action):
        key = Timing.get_caller_identifier()

        # reset latch on first tick
        if self.tick_counter == self.tick_offset:
            action_record = self.timing_records.get(key)
            if action_record is not None:
                self.timing_records.pop(key)

        # process action on subsequent ticks
        if self.tick_counter >= self.tick_offset:
            action_record = self.timing_records.get(key)
            if action_record is None:  # in progress?
                status = action.run(self.tick_counter)
                if status.is_terminal():
                    self.timing_records[key] = TimingRecord(self.tick_counter, status)
                    self.tick_offset = self.tick_counter
                else:
                    self.block()
                return status
            else:  # completed?
                self.tick_offset = action_record.tick
                return action_record.status
        else:  # not started?
            self.block()
            return ActionStatus.NOT_STARTED

    def action_after(self, tick_duration, action):
        self.wait(tick_duration)
        return self.action(action)

    def block(self):
        self.tick_offset = math.inf

    @classmethod
    def get_caller_identifier(cls):
        stack = tb.extract_stack()
        caller_frame = stack[len(stack) - 3]
        return f"{caller_frame.filename}_{caller_frame.name}_{caller_frame.lineno}"

    class PollStatus(Enum):
        ABORTED = 0
