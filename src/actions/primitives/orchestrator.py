from copy import deepcopy

from src.actions.primitives.action import Action
from src.actions.primitives.null import NullAction


class OrchestratorAction(Action):
    def __init__(self, actions, play_count=-1, quit_on_abort=True):
        super().__init__()
        self.action_queue = actions
        self.action_queue.append(NullAction())
        self.play_count = play_count
        self.quit_on_abort = quit_on_abort

        self.original_action_queue = deepcopy(self.action_queue)
        self.original_play_count = play_count

    def first_tick(self):
        pass

    # todo: this code is very similar to Bot.run(). Can we consolidate the two?
    def tick(self, timing):
        if len(self.action_queue) == 1:
            return Action.Status.COMPLETE

        current_action = self.action_queue[0]
        status = current_action.run(timing.tick_counter)

        if self.quit_on_abort and status == Action.Status.ABORTED:
            return Action.Status.COMPLETE

        if status.is_terminal():  # current action is done?
            self.action_queue.pop(0)

            if self.play_count != 0:  # more loops to perform?
                if current_action.play_count > 0:
                    current_action.play_count -= 1
                if current_action.play_count != 0:
                    self.action_queue.append(current_action)

            if isinstance(self.action_queue[0], NullAction):
                self.play_count -= 1
                null_action = self.action_queue.pop(0)
                self.action_queue.append(null_action)

            if self.play_count == 0:
                return Action.Status.COMPLETE

        return Action.Status.IN_PROGRESS

    def last_tick(self):
        # when an action completes, its play_count is decremented, so we need to account for this
        self.play_count = self.original_play_count + 1
        self.action_queue = deepcopy(self.original_action_queue)
