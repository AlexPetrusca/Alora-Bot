from src.actions.primitives.action import Action
from src.robot import robot
from src.robot.timer import Timer
from src.vision.coordinates import TeleportActionCoord, TeleportMenu


class TeleportWizardAction(Action):
    def __init__(self, destination):
        super().__init__()
        if hasattr(destination, 'value'):
            self.destination = destination.value
        else:
            self.destination = destination

    def first_tick(self):
        self.set_progress_message('Walking to Teleport Wizard...')

    def tick(self, timing):
        timing.execute(lambda: robot.click(TeleportActionCoord.TELEPORT_WIZARD))
        timing.execute_after(Timer.sec2tick(5), lambda: (
            self.set_progress_message('Routing to Destination...'),
            robot.click(TeleportMenu.SEARCH)
        ))
        timing.execute_after(Timer.sec2tick(1), lambda: robot.type_text(self.destination))
        timing.execute_after(Timer.sec2tick(1), lambda: (
            self.set_progress_message('Teleporting to Destination...'),
            robot.click(TeleportMenu.FIRST_RESULT)
        ))
        return timing.complete_after(Timer.sec2tick(5))

    def last_tick(self):
        pass

