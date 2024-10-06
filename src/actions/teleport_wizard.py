from src.actions.action import Action
from src.robot import robot
from src.vision.coordinates import TeleportCoord


class TeleportWizardAction(Action):
    destination = ""

    def __init__(self, destination):
        self.destination = destination
        if hasattr(self.destination, 'value'):
            self.destination = destination.value

    def first_tick(self):
        self.set_status('Walking to Teleport Wizard...')

    def tick(self, t):
        if self.tick_counter == 0:
            robot.click(TeleportCoord.TELEPORT_WIZARD)  # teleport wizard
        if self.tick_counter == Action.sec2tick(5):
            self.set_status('Routing to Destination...')
            robot.click(TeleportCoord.SEARCH_BUTTON)  # search
        if self.tick_counter == Action.sec2tick(6):
            robot.press([c for c in self.destination])  # type destination
        if self.tick_counter == Action.sec2tick(7):
            self.set_status('Teleporting to Destination...')
            robot.click(TeleportCoord.SEARCH_FIRST_RESULT)  # go to destination
        return self.tick_counter == Action.sec2tick(12)

    def last_tick(self):
        pass

