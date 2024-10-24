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
    SKELETAL_WYVERN = 'Skeletal Wyvern'


class SlayerAction(Action):
    def __init__(self, task):
        super().__init__()
        self.task = task

        config = SlayerAction.get_task_config(self.task)
        self.potions = config.potions
        self.combat_loop_action = OrchestratorAction([
            CombatAction(
                health_threshold=config.health_threshold,
                dodge_hazards=config.dodge_hazards,
                potions=config.potions
            ),
            PickUpItemsAction()
        ])
        self.prayer_on_action = PrayerAction(*config.prayers)
        self.prayer_off_action = PrayerAction()

    def first_tick(self):
        self.set_progress_message(f'Slaying {self.task.value}s...')

    def tick(self, timing):
        timing.action(self.prayer_on_action)
        timing.action(self.combat_loop_action)
        timing.action(self.prayer_off_action)
        return timing.complete()

    def last_tick(self):
        pass

    @staticmethod
    def get_task_config(task):
        task_configs = {
            SlayerTask.CAVE_KRAKEN: SlayerAction.Config(
                health_threshold=50,
                prayers=[Prayer.PROTECT_FROM_MAGIC, Prayer.MYSTIC_MIGHT]
            ),
            SlayerTask.BASILISK_KNIGHT: SlayerAction.Config(
                health_threshold=75,
                prayers=[Prayer.PROTECT_FROM_MAGIC],
                potions=[Potion.SUPER_COMBAT]
            ),
            SlayerTask.RUNE_DRAGON: SlayerAction.Config(
                health_threshold=50,
                prayers=[Prayer.PROTECT_FROM_MAGIC],
                potions=[Potion.SUPER_COMBAT, Potion.ANTIFIRE]
            ),
            SlayerTask.SKELETAL_WYVERN: SlayerAction.Config(
                health_threshold=50,
                prayers=[Prayer.PROTECT_FROM_MISSILES],
                potions=[Potion.SUPER_COMBAT, Potion.ANTIFIRE]
            ),
        }
        return task_configs[task]

    class Config:
        def __init__(self, health_threshold=50, prayers=None, potions=None, dodge_hazards=False):
            self.health_threshold = health_threshold
            self.prayers = prayers if (prayers is not None) else []
            self.potions = potions if (potions is not None) else []
            self.dodge_hazards = dodge_hazards
