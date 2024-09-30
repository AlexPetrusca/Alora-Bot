from src.actions.barrow import BarrowAction
from src.actions.breadcrumb_trail import BreadcrumbTrailAction
from src.actions.calibrate import CalibrateAction, Direction
from src.actions.cerberus import CerberusAction
from src.actions.heal import HealAction
from src.actions.home_teleport import HomeTeleportAction
from src.actions.pick_up_items import PickUpItemsAction
from src.actions.combat import CombatAction
from src.actions.slayer import SlayerAction
from src.actions.teleport_wizard import TeleportWizardAction
from src.actions.wait import WaitAction
from src.vision.color import Color
from src.vision.coordinates import Prayer


class BotConfig:
    @staticmethod
    def experiment():
        return [
            WaitAction(5).play_once(),

            WaitAction(2),
            BreadcrumbTrailAction()
        ]

    @staticmethod
    def slayer(task, color=Color.YELLOW, health_threshold=30):
        return [
            WaitAction(5).play_once(),
            CalibrateAction().play_once(),

            HomeTeleportAction(),
            TeleportWizardAction(task),

            BreadcrumbTrailAction(color),
            SlayerAction(task, health_threshold),

            HealAction(bank=True)
        ]

    @staticmethod
    def barrows():
        return [
            WaitAction(5).play_once(),
            CalibrateAction().play_once(),

            HomeTeleportAction(),
            TeleportWizardAction("barrows"),

            BarrowAction("A", prayer=Prayer.PROTECT_FROM_MAGIC),
            BarrowAction("K", prayer=Prayer.PROTECT_FROM_MISSILES),
            BarrowAction("G"),
            BarrowAction("D"),
            BarrowAction("V"),
            BarrowAction("T", last=True),

            HomeTeleportAction(),
            HealAction(bank=True)
        ]

    @staticmethod
    def cerberus():
        return [
            WaitAction(5).play_once(),
            CalibrateAction().play_once(),

            HomeTeleportAction(),
            TeleportWizardAction("cerberus"),

            CerberusAction(),

            PickUpItemsAction(),
            HomeTeleportAction(),
            HealAction(bank=True)
        ]
