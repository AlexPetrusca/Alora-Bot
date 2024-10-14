from enum import Enum

from src.actions.prayer import PrayerAction
from src.actions.primitives.action import Action
from src.actions.combat import CombatAction
from src.actions.pick_up_items import PickUpItemsAction
from src.actions.primitives.orchestrator import OrchestratorAction
from src.robot import robot
from src.robot.timing.timer import Timer
from src.vision.coordinates import Prayer, ControlPanel
from src.vision.images import Potion


class SlayerTask(Enum):
    CAVE_KRAKEN = 'Cave Kraken'
    RUNE_DRAGON = 'Rune Dragon'
    BASILISK_KNIGHT = 'Basilisk Knight'


# todo: [bug] sometimes heal action is messed up and fails after tp back
class SlayerAction(Action):
    def __init__(self, task):
        super().__init__()
        self.task = task

        config = SlayerAction.get_task_config(self.task)
        self.potions = config.potions
        self.combat_loop_action = OrchestratorAction([
            CombatAction(health_threshold=config.health_threshold),
            PickUpItemsAction()
        ])
        self.prayer_action = PrayerAction(*config.prayers, switch_inventory=True)

    def first_tick(self):
        self.set_progress_message(f'Slaying {self.task.value}s...')

    def tick(self, timing):
        timing.action(self.prayer_action)
        timing.execute(lambda: robot.click(ControlPanel.INVENTORY_TAB))
        for potion in self.potions:
            timing.execute_after(Timer.sec2tick(1), lambda: robot.click_potion(potion))
        return timing.action(self.combat_loop_action)

    def last_tick(self):
        pass

    @staticmethod
    def get_task_config(task):
        task_configs = {
            SlayerTask.CAVE_KRAKEN: SlayerAction.Config(50, [Prayer.PROTECT_FROM_MAGIC, Prayer.MYSTIC_MIGHT]),
            SlayerTask.BASILISK_KNIGHT: SlayerAction.Config(70, [Prayer.PROTECT_FROM_MAGIC, Prayer.PIETY]),
            SlayerTask.RUNE_DRAGON: SlayerAction.Config(50, [Prayer.PROTECT_FROM_MAGIC, Prayer.PIETY], [Potion.ANTIFIRE]),
        }
        return task_configs[task]

    class Config:
        def __init__(self, health_threshold=50, prayers=None, potions=None):
            self.health_threshold = health_threshold
            self.prayers = prayers if (prayers is not None) else []
            self.potions = potions if (potions is not None) else []
