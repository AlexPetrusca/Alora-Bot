from src.actions.primitives.action import Action
from src.robot import robot
from src.robot.timing.timer import Timer
from src.vision.coordinates import ControlPanel
from src.vision.images import Images
from src.vision.regions import Regions


class AutoRetaliateAction(Action):
    def __init__(self, auto_retaliate=True):
        super().__init__()
        self.auto_retaliate = auto_retaliate

    def first_tick(self):
        self.set_progress_message(f"Setting auto retaliate to {"ON" if self.auto_retaliate else "OFF"}...")

    def tick(self, timing):
        timing.execute(lambda: robot.click(ControlPanel.COMBAT_TAB))
        timing.wait(Timer.sec2tick(0.1))
        if self.auto_retaliate:
            timing.execute(lambda: robot.click_image(Images.Menu.AUTO_RETALIATE_OFF, 0.9, Regions.CONTROL_PANEL))
        else:
            timing.execute(lambda: robot.click_image(Images.Menu.AUTO_RETALIATE_ON, 0.9, Regions.CONTROL_PANEL))
        return timing.complete()

    def last_tick(self):
        pass
