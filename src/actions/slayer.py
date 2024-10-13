from enum import Enum

from src.actions.prayer import PrayerAction
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
        self.prayer_action = PrayerAction(SlayerAction.determine_prayer(task), switch_inventory=True)

    @staticmethod
    def determine_prayer(task):
        magic_tasks = {SlayerTask.CAVE_KRAKEN, SlayerTask.RUNE_DRAGON, SlayerTask.BASILISK_KNIGHT}
        melee_tasks = {}
        ranged_tasks = {}
        if task in magic_tasks:
            return Prayer.PROTECT_FROM_MAGIC
        elif task in ranged_tasks:
            return Prayer.PROTECT_FROM_MISSILES
        elif task in melee_tasks:
            return Prayer.PROTECT_FROM_MELEE
        else:
            raise AssertionError(f"No prayer mapped to slayer task: {task}")

    def first_tick(self):
        self.set_progress_message(f'Slaying {self.task.value}s...')

    def tick(self, timing):
        timing.action(self.prayer_action)
        return timing.action(self.combat_loop_action)

    def last_tick(self):
        pass
