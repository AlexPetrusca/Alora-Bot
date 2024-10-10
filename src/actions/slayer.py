from enum import Enum

from src.actions.primitives.action import Action
from src.actions.combat import CombatAction
from src.actions.pick_up_items import PickUpItemsAction
from src.actions.primitives.orchestrator import OrchestratorAction
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
        self.combat_loop_action = OrchestratorAction([
            CombatAction(health_threshold=self.health_threshold),
            PickUpItemsAction()
        ])

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
        timing.execute(lambda: robot.click(ControlPanel.PRAYER_TAB))
        timing.execute_after(Timer.sec2tick(0.5), lambda: robot.click(self.prayer))
        timing.execute_after(Timer.sec2tick(0.5), lambda: robot.click(ControlPanel.INVENTORY_TAB))
        return timing.action(self.combat_loop_action)

    def last_tick(self):
        pass
