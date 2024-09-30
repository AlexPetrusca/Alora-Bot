from enum import Enum

from src.actions.action import Action
from src.actions.combat import CombatAction
from src.actions.pick_up_items import PickUpItemsAction
from src.util import robot
from src.vision.coordinates import Prayer, Controls


class SlayerTask(Enum):
    CAVE_KRAKEN = 'Cave Kraken'
    RUNE_DRAGON = 'Rune Dragon'


class SlayerAction(Action):
    task = None
    prayer = None

    action_queue = []
    tp_home_tick = None
    t_ref = 0

    def __init__(self, task):
        self.task = task

        # implement fully
        if self.task == SlayerTask.CAVE_KRAKEN or self.task == SlayerTask.RUNE_DRAGON:
            self.prayer = Prayer.PROTECT_FROM_MAGIC
        # elif :
        #     self.prayer = Prayer.PROTECT_FROM_MAGIC
        else:
            self.prayer = Prayer.PROTECT_FROM_MELEE

        self.action_queue = [
            CombatAction(),
            PickUpItemsAction(pause_on_fail=False)
        ]

    def first_tick(self):
        self.set_status(f'Slaying {self.task.value}s...')

    def tick(self, t):
        dt = t - self.t_ref
        if self.tick_counter == 0:
            robot.click(Controls.PRAYER_TAB)
        if self.tick_counter == Action.sec2tick(0.5):
            robot.click(self.prayer)
        if self.tick_counter == Action.sec2tick(1):
            robot.click(Controls.INVENTORY_TAB)

        top = self.action_queue[0]
        if top.run(dt):
            if self.tp_home_tick is not None:
                return True
            self.action_queue.pop(0)
            self.action_queue.append(top)
            self.t_ref = t

        if top.did_tp_home():
            self.tp_home_tick = self.tick_counter

        return False

    def last_tick(self):
        self.action_queue = [
            CombatAction(),
            PickUpItemsAction(pause_on_fail=False)
        ]
        self.tp_home_tick = None
        self.t_ref = 0
