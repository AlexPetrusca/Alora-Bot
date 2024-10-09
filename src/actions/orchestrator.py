from src.actions.action import Action


class OrchestratorAction(Action):
    play_count = -1
    loop_length = 0
    quit_on_abort = True

    action_queue = []
    action_count = 0

    def __init__(self, actions, play_count=-1, quit_on_abort=True):
        self.action_queue = actions
        self.play_count = play_count
        self.quit_on_abort = quit_on_abort

        self.loop_length = 0
        for action in self.action_queue:
            if action.play_count == -1:
                self.loop_length += 1

    def first_tick(self):
        pass

    # todo: this code is very similar to Bot.run(). Can we consolidate the two?
    def tick(self):
        if len(self.action_queue) == 0:
            return Action.Status.COMPLETE

        current_action = self.action_queue[0]
        status = current_action.run(self.tick_counter)

        if self.quit_on_abort and status == Action.Status.ABORTED:
            return Action.Status.COMPLETE

        if status.is_terminal():  # current action is done?
            self.action_queue.pop(0)
            if current_action.play_count == -1:
                self.action_count += 1
            if self.action_count / self.loop_length != self.play_count:  # more loops to perform?
                if current_action.play_count > 0:
                    current_action.play_count -= 1
                if current_action.play_count != 0:
                    self.action_queue.append(current_action)
            else:
                return Action.Status.COMPLETE

        return Action.Status.IN_PROGRESS

    def last_tick(self):
        pass
