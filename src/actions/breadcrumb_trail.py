import mss

from src.actions.action import Action
from src.util import robot
from src.vision import vision
from src.vision.color import Color


class BreadcrumbTrailAction(Action):
    color = Color.YELLOW
    sct = mss.mss()

    dest_tile = None

    def __init__(self, color=Color.YELLOW):
        self.color = color

    def first_tick(self):
        self.set_status(f'Following {self.color} breadcrumb trail...')

    # todo: try different color for destination marker to try to make it thinner
    # todo: wait about a second after dest_tile disappears before clicking next breadcrumb
    def tick(self, t):
        if self.tick_counter % Action.sec2tick(1) == 0:
            dest_tile = vision.locate_contour(vision.grab_screen(self.sct), Color.WHITE)
            print("White Tile:", dest_tile)
            if dest_tile is None:
                clicked_breadcrumb = robot.click_contour(self.color, min_distance=50)
                print("Yellow Tile:", clicked_breadcrumb)
                if not clicked_breadcrumb:
                    return True  # reached destination

        return False

    def last_tick(self):
        self.dest_tile = None
