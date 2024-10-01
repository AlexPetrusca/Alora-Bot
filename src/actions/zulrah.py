import mss

from src.actions.action import Action
from src.util import robot
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import Controls, Prayer
from src.vision.vision import ContourDetection


class ZulrahAction(Action):
    sct = mss.mss()

    zulrah_color = None
    color_change_tick = 0

    def first_tick(self):
        self.set_status(f'Fighting Zulrah...')

    def tick(self, t):
        if self.tick_counter % Action.sec2tick(1) == 0:
            screenshot = vision.grab_screen(self.sct, hide_ui=True)
            red_contour, red_area = vision.get_contour(screenshot, Color.RED, mode=ContourDetection.AREA_LARGEST)
            green_contour, green_area = vision.get_contour(screenshot, Color.GREEN, mode=ContourDetection.AREA_LARGEST)
            blue_contour, blue_area = vision.get_contour(screenshot, Color.BLUE, mode=ContourDetection.AREA_LARGEST)

            max_area, max_color = 0, None
            if red_area > max_area:
                max_area, max_color = red_area, Color.RED
            if green_area > max_area:
                max_area, max_color = green_area, Color.GREEN
            if blue_area > max_area:
                max_area, max_color = blue_area, Color.BLUE

            if self.zulrah_color is None and max_color is not None:
                self.color_change_tick = self.tick_counter
                self.zulrah_color = max_color
                print(max_color, '-->', max_area)
            elif self.zulrah_color is not None and max_color is None:
                self.zulrah_color = None

        tick_offset = self.color_change_tick
        if self.tick_counter == tick_offset:
            robot.click(Controls.PRAYER_TAB)
        tick_offset += Action.sec2tick(0.5)
        if self.tick_counter == tick_offset:
            if self.zulrah_color == Color.GREEN:
                robot.click(Prayer.PROTECT_FROM_MISSILES)
            elif self.zulrah_color == Color.BLUE:
                robot.click(Prayer.PROTECT_FROM_MAGIC)
            elif self.zulrah_color == Color.RED:
                robot.click(Prayer.PROTECT_FROM_MELEE)
        tick_offset += Action.sec2tick(1)
        if self.tick_counter == tick_offset:
            robot.click(Controls.INVENTORY_TAB)

        return False

    def last_tick(self):
        self.zulrah_color = None
        self.color_change_tick = 0
