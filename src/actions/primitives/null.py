from src.actions.primitives.action import Action


class NullAction(Action):
    def first_tick(self):
        pass

    def tick(self):
        return Action.Status.COMPLETE

    def last_tick(self):
        pass
