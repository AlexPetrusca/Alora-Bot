import cv2 as cv
import mss

from src.actions.action import Action
from src.util import robot
from src.vision import vision


class ClickImageAction(Action):
    sct = mss.mss()
    image = None

    def __init__(self, image_url):
        self.image = cv.imread(image_url, cv.IMREAD_UNCHANGED)

    def first_tick(self):
        pass

    def tick(self, t):
        screenshot = vision.grab_screen(self.sct)
        x, y = vision.locate_image(screenshot, self.image)  # todo: this blows up if the image isn't found
        robot.click(x / 2, y / 2)
        return True

    def last_tick(self):
        pass
