from enum import Enum


class ActionStatus(Enum):
    NOT_STARTED = 1
    IN_PROGRESS = 2
    ABORTED = 3
    COMPLETE = 4

    def is_terminal(self):
        return self == ActionStatus.COMPLETE or self == ActionStatus.ABORTED
