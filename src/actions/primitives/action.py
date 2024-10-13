import logging
from abc import abstractmethod
from src.actions.types.action_status import ActionStatus
from src.robot.timing.timing import Timing


class Action:
    def __init__(self):
        self.timing = Timing()
        self.play_count = -1
        self.progress_message = ""

    @abstractmethod
    def first_tick(self):
        ...

    @abstractmethod
    def tick(self, timing: Timing):
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

        return ActionStatus.IN_PROGRESS

    def set_progress_message(self, progress_message):
        self.progress_message = progress_message
        logging.info(self.progress_message)

    def play(self, count):
        self.play_count = count
        return self

    def play_once(self):
        return self.play(1)
