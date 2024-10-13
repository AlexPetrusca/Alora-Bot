from src.actions.primitives.action import Action
from src.actions.types.action_status import ActionStatus


class NullAction(Action):
    def first_tick(self):
        pass

    def tick(self, timing):
        return ActionStatus.COMPLETE

    def last_tick(self):
        pass
