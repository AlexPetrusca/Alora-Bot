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
        if timing.tick_counter == 0:
            robot.click(TeleportActionCoord.TELEPORT_WIZARD)  # teleport wizard
        if timing.tick_counter == Timer.sec2tick(5):
            self.set_progress_message('Routing to Destination...')
            robot.click(TeleportMenu.SEARCH)  # search
        if timing.tick_counter == Timer.sec2tick(6):
            robot.press([c for c in self.destination])  # type destination
        if timing.tick_counter == Timer.sec2tick(7):
            self.set_progress_message('Teleporting to Destination...')
            robot.click(TeleportMenu.FIRST_RESULT)  # go to destination
        if timing.tick_counter == Timer.sec2tick(12):
            return Action.Status.COMPLETE
        return Action.Status.IN_PROGRESS

    def last_tick(self):
        pass

