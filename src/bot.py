import logging
import threading
import mss
from time import perf_counter
from src.actions.calibrate import CalibrateAction
from src.actions.wait import WaitAction
from src.debug import DebugDisplay


class Bot:
    debug_display = False
    loop = False

    action_queue = []
    t_ref = perf_counter()

    def __init__(self, loop=False, debug=False):
        self.debug_display = debug
        self.loop = loop

        self.action_queue.append(WaitAction(5))
        self.action_queue.append(CalibrateAction())
        self.action_queue.append(TeleportHomeAction())

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
            self.debug_display = DebugDisplay()
        while True:
            if self.debug_display:
                self.debug_display.show(perf_counter())
            if self.tick():
                logging.info("Done!")
                return
