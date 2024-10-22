from src.actions.barrow import BarrowAction, BarrowBrother
from src.actions.breadcrumb_trail import BreadcrumbTrailAction
from src.actions.calibrate import CalibrateAction, Direction
from src.actions.cerberus import CerberusAction
from src.actions.demonic_gorillas import DemonicGorillaAction
from src.actions.experiment import ExperimentAction
from src.actions.gear_switch import GearSwitchAction, GearSwitch
from src.actions.heal import HealAction
from src.actions.home_teleport import HomeTeleportAction
from src.actions.prayer import PrayerAction
from src.actions.primitives.orchestrator import OrchestratorAction
from src.actions.pick_up_items import PickUpItemsAction
from src.actions.combat import CombatAction
from src.actions.sarachnis import SarachnisAction
from src.actions.slayer import SlayerAction
from src.actions.teleport_wizard import TeleportWizardAction
from src.actions.tormented_demon import TormentedDemonAction
from src.actions.wait import WaitAction
from src.actions.zulrah import ZulrahAction
from src.vision.color import Color
from src.vision.coordinates import Prayer
from src.vision.images import Gear


class BotConfig:
    @staticmethod
    def experiment():
        return [
            WaitAction(1).play_once(),

            # ExperimentAction(),
            # BreadcrumbTrailAction(dangerous=True),

            # TormentedDemonAction(),
            # DemonicGorillaAction(),
            # SarachnisAction(),
            # ZulrahAction(),
            CombatAction(target=None),
            # PickUpItemsAction(),
        ]

    @staticmethod
    def combat():
        return [
            WaitAction(5).play_once(),

            CombatAction(),
            PickUpItemsAction()
        ]

    @staticmethod
    def slayer(task, trail_color=Color.YELLOW):
        return [
            WaitAction(5).play_once(),
            CalibrateAction().play_once(),

            HomeTeleportAction(),
            TeleportWizardAction(task),

            BreadcrumbTrailAction(trail_color),
            SlayerAction(task),

            HealAction(bank=True)
        ]

    @staticmethod
    def sarachnis():
        return [
            WaitAction(5).play_once(),
            CalibrateAction().play_once(),

            HomeTeleportAction(),
            TeleportWizardAction("Sarachnis"),

            CalibrateAction(Direction.SOUTH),
            BreadcrumbTrailAction(Color.YELLOW, target=4, dangerous=True),
            OrchestratorAction([
                SarachnisAction(),
                PickUpItemsAction(),
            ]),

            CalibrateAction(Direction.NORTH),
            HealAction(bank=True)
        ]

    @staticmethod
    def demonic_gorillas():
        return [
            WaitAction(5).play_once(),
            CalibrateAction().play_once(),

            HomeTeleportAction(),
            TeleportWizardAction("Gorillas"),

            BreadcrumbTrailAction(Color.YELLOW),
            OrchestratorAction([
                DemonicGorillaAction(),
                PickUpItemsAction(),
            ]),

            HealAction(bank=True)
        ]

    @staticmethod
    def barrows():
        return [
            WaitAction(5).play_once(),
            CalibrateAction().play_once(),

            HomeTeleportAction(),
            TeleportWizardAction("Barrows"),

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
            TeleportWizardAction("Cerberus"),

            CerberusAction(),

            PickUpItemsAction(),
            HomeTeleportAction(),
            HealAction(bank=True)
        ]
