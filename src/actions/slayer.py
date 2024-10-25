from src.actions.prayer import PrayerAction
from src.actions.primitives.action import Action
from src.actions.combat.combat import CombatAction
from src.actions.pick_up_items import PickUpItemsAction
from src.actions.primitives.orchestrator import OrchestratorAction
from src.vision.coordinates import Prayer
from src.vision.images import Potion


class SlayerTask:
    class Config:
        def __init__(self, tp_target, prayers, combat_action):
            self.tp_target = tp_target
            self.prayers = prayers
            self.combat_action = combat_action

    CAVE_KRAKEN = Config(
        tp_target='Cave Kraken',
        prayers=[Prayer.PROTECT_FROM_MAGIC, Prayer.MYSTIC_MIGHT],
        combat_action=CombatAction(),
    )
    RUNE_DRAGON = Config(
        tp_target='Rune Dragon',
        prayers=[Prayer.PROTECT_FROM_MAGIC],
        combat_action=CombatAction(
            potions=[Potion.SUPER_COMBAT, Potion.ANTIFIRE]
        ),
    )
    BASILISK_KNIGHT = Config(
        tp_target='Basilisk Knight',
        prayers=[Prayer.PROTECT_FROM_MAGIC],
        combat_action=CombatAction(
            health_threshold=75,
            potions=[Potion.SUPER_COMBAT]
        ),
    )
    SKELETAL_WYVERN = Config(
        tp_target='Skeletal Wyvern',
        prayers=[Prayer.PROTECT_FROM_MAGIC],
        combat_action=CombatAction(
            potions=[Potion.SUPER_COMBAT, Potion.ANTIFIRE]
        ),
    )
    VAMPYRE = Config(
        tp_target='Vampyre',
        prayers=[Prayer.PROTECT_FROM_MELEE],
        combat_action=CombatAction(
            potions=[Potion.SUPER_COMBAT]
        ),
    )


class SlayerAction(Action):
    def __init__(self, task):
        super().__init__()
        self.task = task

        self.combat_loop_action = OrchestratorAction([
            task.combat_action,
            PickUpItemsAction()
        ])
        self.prayer_on_action = PrayerAction(*task.prayers)
        self.prayer_off_action = PrayerAction()

    def first_tick(self):
        # self.set_progress_message(f'Slaying {self.task.value}s...')
        pass

    def tick(self, timing):
        timing.action(self.prayer_on_action)
        timing.action(self.combat_loop_action)
        timing.action(self.prayer_off_action)
        return timing.complete()

    def last_tick(self):
        pass
