import logging
import threading
import mss
from time import perf_counter

from src.actions.barrow import BarrowAction
from src.actions.calibrate import CalibrateAction
from src.actions.cerberus import CerberusAction
from src.actions.heal import HealAction
from src.actions.home_teleport import HomeTeleportAction
from src.actions.pick_up_items import PickUpItemsAction
from src.actions.slayer import SlayerAction
from src.actions.teleport_wizard import TeleportWizardAction
from src.actions.wait import WaitAction
from src.debug import DebugDisplay
from src.vision.coordinates import Prayer


class Bot:
    debug_display = False
    loop = False

    action_queue = []
    t_ref = perf_counter()

    def __init__(self, loop=False, debug=False):
        self.debug_display = debug
        self.loop = loop

        ''' Cerberus '''
        # self.action_queue.append(WaitAction(5))
        # self.action_queue.append(HomeTeleportAction())
        # self.action_queue.append(CalibrateAction())
        # self.action_queue.append(TeleportWizardAction("cerberus"))
        #
        # self.action_queue.append(CerberusAction())
        #
        # self.action_queue.append(PickUpItemsAction())
        # self.action_queue.append(HomeTeleportAction())
        # self.action_queue.append(HealAction(bank=True))  # todo: a heal action should probably include a home teleport action

        ''' Slayer '''
        # self.action_queue.append(SlayerAction())
        # self.action_queue.append(PickUpItemsAction())

        ''' Barrows '''
        self.action_queue.append(WaitAction(5))
        self.action_queue.append(HomeTeleportAction())
        self.action_queue.append(CalibrateAction())
        self.action_queue.append(TeleportWizardAction("barrows"))

        self.action_queue.append(BarrowAction("A", prayer=Prayer.PROTECT_FROM_MAGIC))
        self.action_queue.append(BarrowAction("K", prayer=Prayer.PROTECT_FROM_MISSILES))
        self.action_queue.append(BarrowAction("G"))
        self.action_queue.append(BarrowAction("D"))
        self.action_queue.append(BarrowAction("V"))
        self.action_queue.append(BarrowAction("T", last=True))

        self.action_queue.append(HomeTeleportAction())
        self.action_queue.append(HealAction(bank=True))  # todo: a heal action should probably include a home teleport action

    def tick(self):
        t = perf_counter() - self.t_ref
        if len(self.action_queue) == 0:  # actions is done?
            return True
        elif self.action_queue[0].run(t):  # current action is done?
            self.t_ref = perf_counter()
            top = self.action_queue.pop(0)
            if self.loop:
                self.action_queue.append(top)
        return False

    def start(self):
        if self.debug_display:
            self.debug_display = DebugDisplay(self)
        while True:
            if self.debug_display:
                self.debug_display.show(perf_counter())
            if self.tick():
                logging.info("Done!")
                return
