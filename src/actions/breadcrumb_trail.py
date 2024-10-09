import mss

from src.actions.primitives.action import Action
from src.robot import robot
from src.robot.timer import Timer
from src.vision import vision
from src.vision.color import Color
from src.vision.images import Images


# todo: [bug] sometimes gets stuck before final breadcrumb (maybe related to todo below)
class BreadcrumbTrailAction(Action):
    sct = mss.mss()

    def __init__(self, color=Color.YELLOW):
        super().__init__()
        self.color = color

        self.next_label = 0
        self.retry_count = 0

    def first_tick(self):
        self.set_progress_message(f'Following {self.color.to_string()} breadcrumb trail...')

    # todo: wait about a second after dest_tile disappears before clicking next breadcrumb
    def tick(self):
        if self.tick_counter % Timer.sec2tick(1) == 0:
            screenshot = vision.grab_screen(self.sct, hide_ui=True)
            dest_tile = vision.locate_contour(screenshot, Color.WHITE)
            if dest_tile is None:
                breadcrumb_loc = vision.locate_image(screenshot, Images.YELLOW_MARKERS[self.next_label], 0.8)
                if breadcrumb_loc is not None:
                    robot.click(breadcrumb_loc[0] / 2, breadcrumb_loc[1] / 2)
                    self.next_label += 1
                    self.retry_count = 0
                else:
                    print("Failed looking for breadcrumb: ", self.next_label)
                    self.retry_count += 1
                    if self.retry_count >= 4:
                        return Action.Status.COMPLETE  # reached destination

        return Action.Status.IN_PROGRESS

    def last_tick(self):
        self.next_label = 0
        self.retry_count = 0
