from enum import Enum

from src.actions.primitives.action import Action
from src.actions.combat import CombatAction
from src.actions.pick_up_items import PickUpItemsAction
from src.robot import robot
from src.robot.timer import Timer
from src.vision.coordinates import Prayer, ControlPanel


class SlayerTask(Enum):
    CAVE_KRAKEN = 'Cave Kraken'
    RUNE_DRAGON = 'Rune Dragon'
    BASILISK_KNIGHT = 'Basilisk Knight'


# todo: [bug] sometimes heal action is messed up and fails after tp back
class SlayerAction(Action):
    def __init__(self, task, health_threshold=30):
        super().__init__()
        self.task = task
        self.health_threshold = health_threshold
        self.action_queue = [
            CombatAction(health_threshold=self.health_threshold),
            PickUpItemsAction()
        ]

        magic_tasks = {SlayerTask.CAVE_KRAKEN, SlayerTask.RUNE_DRAGON, SlayerTask.BASILISK_KNIGHT}
        melee_tasks = {}
        ranged_tasks = {}

        self.prayer = Prayer.PROTECT_FROM_MELEE
        if task in magic_tasks:
            self.prayer = Prayer.PROTECT_FROM_MAGIC
        elif task in ranged_tasks:
            self.prayer = Prayer.PROTECT_FROM_MISSILES
        elif task in melee_tasks:
            self.prayer = Prayer.PROTECT_FROM_MELEE

    def first_tick(self):
        self.set_progress_message(f'Slaying {self.task.value}s...')

    def tick(self, timing):
        if timing.tick_counter == 0:
            robot.click(ControlPanel.PRAYER_TAB)
        if timing.tick_counter == Timer.sec2tick(0.5):
            robot.click(self.prayer)
        if timing.tick_counter == Timer.sec2tick(1):
            robot.click(ControlPanel.INVENTORY_TAB)

        top = self.action_queue[0]
        status = top.run(timing.tick_counter)
        if status == Action.Status.COMPLETE:
            self.action_queue.pop(0)
            self.action_queue.append(top)
        elif status == Action.Status.ABORTED:
            return Action.Status.COMPLETE

        return Action.Status.IN_PROGRESS

    def last_tick(self):
        self.action_queue = [
            CombatAction(health_threshold=self.health_threshold),
            PickUpItemsAction()
        ]
