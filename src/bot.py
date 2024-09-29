import logging
from time import perf_counter

from src.actions.barrow import BarrowAction
from src.actions.calibrate import CalibrateAction
from src.actions.cerberus import CerberusAction
from src.actions.heal import HealAction
from src.actions.home_teleport import HomeTeleportAction
from src.actions.pick_up_items import PickUpItemsAction
from src.actions.combat import CombatAction
from src.actions.teleport_wizard import TeleportWizardAction
from src.actions.wait import WaitAction
from src.background import BackgroundScript
from src.debug import DebugDisplay
from src.keylogger.keys import Key
from src.vision.coordinates import Prayer


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

        config = self.config_test
        # config = self.config_cerberus
        # config = self.config_combat
        # config = self.config_barrows
        self.apply_config(config)

    def apply_config(self, config_fn):
        self.action_queue.clear()
        config_fn()

        self.current_config = config_fn
        self.current_action = self.action_queue[0]

        self.loop_length = 0
        for action in self.action_queue:
            if action.play_count == -1:
                self.loop_length += 1

    def config_test(self):
        self.action_queue.append(WaitAction(5).play_once())

        self.action_queue.append(WaitAction(2))
        self.action_queue.append(WaitAction(1))

    def config_barrows(self):
        self.action_queue.append(WaitAction(5).play_once())
        self.action_queue.append(CalibrateAction().play_once())

        self.action_queue.append(HomeTeleportAction())
        self.action_queue.append(TeleportWizardAction("barrows"))

        self.action_queue.append(BarrowAction("A", prayer=Prayer.PROTECT_FROM_MAGIC))
        self.action_queue.append(BarrowAction("K", prayer=Prayer.PROTECT_FROM_MISSILES))
        self.action_queue.append(BarrowAction("G"))
        self.action_queue.append(BarrowAction("D"))
        self.action_queue.append(BarrowAction("V"))
        self.action_queue.append(BarrowAction("T", last=True))

        self.action_queue.append(HomeTeleportAction())
        self.action_queue.append(HealAction(bank=True))  # todo: heal action should probably include a home teleport

    def config_combat(self):
        self.action_queue.append(WaitAction(5).play_once())

        self.action_queue.append(CombatAction())
        self.action_queue.append(PickUpItemsAction(pause_on_fail=False))

    def config_cerberus(self):
        self.action_queue.append(WaitAction(5).play_once())
        self.action_queue.append(CalibrateAction().play_once())

        self.action_queue.append(HomeTeleportAction())
        self.action_queue.append(TeleportWizardAction("cerberus"))

        self.action_queue.append(CerberusAction())

        self.action_queue.append(PickUpItemsAction())
        self.action_queue.append(HomeTeleportAction())
        self.action_queue.append(HealAction(bank=True))  # todo: heal action should probably include a home teleport

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
