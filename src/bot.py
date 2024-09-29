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
from src.debug import DebugDisplay
from src.vision.coordinates import Prayer


class Bot:
    debug = False
    play_count = -1

    action_queue = []
    loop_length = 0
    action_count = 0
    t_old = perf_counter()

    def __init__(self, play_count=-1, debug=False):
        self.debug = debug
        self.play_count = play_count

        config = self.config_test
        # config = self.config_cerberus
        # config = self.config_combat
        # config = self.config_barrows
        self.apply_config(config)

    def apply_config(self, config_fn):
        self.action_queue.clear()
        config_fn()
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

    def tick(self):
        t = perf_counter() - self.t_old
        if len(self.action_queue) == 0:  # all actions are done?
            return True
        elif self.action_queue[0].run(t):  # current action is done?
            self.t_old = perf_counter()
            top = self.action_queue.pop(0)
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
            if self.debug:
                self.debug.tick(perf_counter())
            if self.tick():
                logging.info("Done!")
                return
