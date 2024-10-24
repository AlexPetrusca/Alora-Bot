import logging
from copy import deepcopy
from enum import Enum

from src.actions.primitives.null import NullAction
from src.actions.slayer import SlayerTask
from src.background import BackgroundScript
from src.bot_config import BotConfig
from src.debug import DebugDisplay
from src.keylogger.keys import Key
from src.robot.timing.timer import Timer


class Bot:
    def __init__(self, play_count=-1, debug=False):
        self.timer = Timer()
        self.background = BackgroundScript(self)
        self.play_count = play_count
        self.debug = debug
        self.paused = False

        self.action_queue = []
        self.current_config = None
        self.current_action = None

        # config = BotConfig.experiment()
        # config = BotConfig.combat()
        # config = BotConfig.slayer(SlayerTask.BASILISK_KNIGHT)
        config = BotConfig.slayer(SlayerTask.CAVE_KRAKEN)
        # config = BotConfig.slayer(SlayerTask.RUNE_DRAGON)
        # config = BotConfig.slayer(SlayerTask.SKELETAL_WYVERN)
        # config = BotConfig.sarachnis()
        # config = BotConfig.demonic_gorillas()
        # config = BotConfig.cerberus()
        # config = BotConfig.barrows()
        self.apply_config(config)

    def apply_config(self, config):
        self.action_queue = deepcopy(config)
        self.action_queue.append(NullAction())
        self.current_config = config
        self.current_action = self.action_queue[0]

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
        if len(self.action_queue) == 1:
            return Bot.Status.DONE
        if self.paused:  # paused?
            return Bot.Status.PAUSED

        status = self.current_action.run(self.timer.tick_counter)
        if status.is_terminal():  # current action is done?
            top = self.action_queue.pop(0)

            if self.play_count != 0:  # more loops to perform?
                if top.play_count > 0:
                    top.play_count -= 1
                if top.play_count != 0:
                    self.action_queue.append(top)

            if isinstance(self.action_queue[0], NullAction):
                logging.info("")
                self.play_count -= 1
                null_action = self.action_queue.pop(0)
                self.action_queue.append(null_action)

            self.current_action = self.action_queue[0]

            if self.play_count == 0:
                return Bot.Status.DONE

        return Bot.Status.WORKING

    def start(self):
        if self.debug:
            self.debug = DebugDisplay(self)
        while True:
            self.background.run()
            if self.debug:
                self.debug.run()

            self.handle_user_input()
            if self.timer.run() == Timer.Status.TICK:  # did timer tick?
                if self.run() == Bot.Status.DONE:  # is bot done?
                    logging.info("Done!")
                    return

    class Status(Enum):
        PAUSED = 0
        WORKING = 1
        DONE = 2
