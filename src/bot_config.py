from src.actions.barrow import BarrowAction, BarrowBrother
from src.actions.breadcrumb_trail import BreadcrumbTrailAction
from src.actions.calibrate import CalibrateAction
from src.actions.cerberus import CerberusAction
from src.actions.heal import HealAction
from src.actions.home_teleport import HomeTeleportAction
from src.actions.primitives.orchestrator import OrchestratorAction
from src.actions.pick_up_items import PickUpItemsAction
from src.actions.combat import CombatAction
from src.actions.slayer import SlayerAction
from src.actions.teleport_wizard import TeleportWizardAction
from src.actions.wait import WaitAction
from src.actions.zulrah import ZulrahAction
from src.vision.color import Color
from src.vision.coordinates import Prayer


class BotConfig:
    @staticmethod
    def experiment():
        return [
            WaitAction(1).play_once(),

            ZulrahAction()
        ]

    @staticmethod
    def combat():
        return [
            WaitAction(5).play_once(),

            CombatAction(),
            PickUpItemsAction()
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

            BarrowAction(BarrowBrother.AHRIM, prayer=Prayer.PROTECT_FROM_MAGIC),
            BarrowAction(BarrowBrother.KARIL, prayer=Prayer.PROTECT_FROM_MISSILES),
            BarrowAction(BarrowBrother.GUTHAN),
            BarrowAction(BarrowBrother.DHAROK),
            BarrowAction(BarrowBrother.VERAC),
            BarrowAction(BarrowBrother.TORAG, last=True),

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
