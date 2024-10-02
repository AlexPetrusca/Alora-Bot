import logging
from copy import copy
from time import perf_counter

from src.actions.slayer import SlayerTask
from src.background import BackgroundScript
from src.bot_config import BotConfig
from src.debug import DebugDisplay
from src.keylogger.keys import Key


class Bot:
    background = None
    play_count = -1
    debug = False
    paused = False

    action_queue = []
    current_config = None
    current_action = None
    loop_length = 0
    action_count = 0

    t_start = perf_counter()
    t_duration = 0

    def __init__(self, play_count=-1, debug=False):
        self.debug = debug
        self.play_count = play_count
        self.background = BackgroundScript(self)

        # config = BotConfig.experiment()
        # config = BotConfig.slayer(SlayerTask.BASILISK_KNIGHT, health_threshold=70)
        # config = BotConfig.slayer(SlayerTask.CAVE_KRAKEN, health_threshold=40)
        # config = BotConfig.cerberus()
        config = BotConfig.barrows()
        self.apply_config(config)

    def apply_config(self, config):
        self.action_queue = copy(config)
        self.current_config = config
        self.current_action = self.action_queue[0]

        self.loop_length = 0
        for action in self.action_queue:
            if action.play_count == -1:
                self.loop_length += 1

    # todo: [bug] Pausing then resetting then playing skips actions (reset is broken)
    def handle_user_input(self):
        if self.paused != self.background.key_toggled(Key.F1):  # pause/play
            self.paused = self.background.key_toggled(Key.F1)
            if self.paused:
                logging.info("Pause")
            else:
                self.t_start = perf_counter() - self.t_duration
                logging.info("Play")
        if self.background.key_toggled(Key.F2):  # reset
            logging.info("Reset")
            self.apply_config(self.current_config)
            self.t_start = perf_counter()
            self.t_duration = 0
            self.background.untoggle_key(Key.F2)
        if self.background.key_toggled(Key.F3):  # exit
            logging.info("Exit")
            exit(1)

    def tick(self):
        self.handle_user_input()
        if len(self.action_queue) == 0:  # all actions are done?
            return True
        if self.paused:
            return False

        self.t_duration = perf_counter() - self.t_start
        if self.current_action.run(self.t_duration):  # current action is done?
            self.t_start = perf_counter()
            top = self.action_queue.pop(0)
            self.current_action = self.action_queue[0]
            if top.play_count == -1:
                self.action_count += 1
            if self.action_count / self.loop_length != self.play_count:  # all replays are done?
                if top.play_count > 0:
                    top.play_count -= 1
                if top.play_count != 0:
                    self.action_queue.append(top)
            else:
                return True

        return False

    def start(self):
        if self.debug:
            self.debug = DebugDisplay(self)
        while True:
            self.background.tick(perf_counter())
            if self.debug:
                self.debug.tick(perf_counter())
            if self.tick():
                logging.info("Done!")
                return
