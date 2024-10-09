import logging
from copy import deepcopy

from src.actions.slayer import SlayerTask
from src.background import BackgroundScript
from src.bot_config import BotConfig
from src.debug import DebugDisplay
from src.keylogger.keys import Key
from src.robot.timer import Timer


class Bot:
    timer = None
    background = None
    play_count = -1
    debug = False
    paused = False

    action_queue = []
    current_config = None
    current_action = None
    loop_length = 0
    action_count = 0

    def __init__(self, play_count=-1, debug=False):
        self.timer = Timer()
        self.background = BackgroundScript(self)
        self.play_count = play_count
        self.debug = debug

        config = BotConfig.experiment()
        # config = BotConfig.combat()
        # config = BotConfig.slayer(SlayerTask.BASILISK_KNIGHT, health_threshold=70)
        # config = BotConfig.slayer(SlayerTask.CAVE_KRAKEN, health_threshold=40)
        # config = BotConfig.cerberus()
        # config = BotConfig.barrows()
        self.apply_config(config)

    def apply_config(self, config):
        self.action_queue = deepcopy(config)
        self.current_config = config
        self.current_action = self.action_queue[0]

        self.loop_length = 0
        for action in self.action_queue:
            if action.play_count == -1:
                self.loop_length += 1

    def handle_user_input(self):
        if self.paused != self.background.key_toggled(Key.F1):  # pause/play
            self.paused = self.background.key_toggled(Key.F1)
            if self.paused:
                logging.info("Pause")
                self.timer.pause()
            else:
                logging.info("Play")
                self.timer.play()
        if self.background.key_toggled(Key.F2):  # reset
            logging.info("Reset")
            self.timer.reset()
            self.apply_config(self.current_config)
            self.background.untoggle_key(Key.F2)
        if self.background.key_toggled(Key.F3):  # exit
            logging.info("Exit")
            exit(1)

    def run(self):
        self.handle_user_input()
        if len(self.action_queue) == 0:  # all actions are done?
            return True
        if self.paused:  # paused?
            return False

        status = self.current_action.run(self.timer.tick_counter)
        if status.is_terminal():  # current action is done?
            top = self.action_queue.pop(0)

            if top.play_count == -1:
                self.action_count += 1
            if self.action_count / self.loop_length != self.play_count:  # more loops to perform?
                if top.play_count > 0:
                    top.play_count -= 1
                if top.play_count != 0:
                    self.action_queue.append(top)
            else:
                return True

            self.current_action = self.action_queue[0]

        return False

    def start(self):
        if self.debug:
            self.debug = DebugDisplay(self)
        while True:
            self.timer.run()
            self.background.run()
            if self.debug:
                self.debug.run()
            if self.run():
                logging.info("Done!")
                return
