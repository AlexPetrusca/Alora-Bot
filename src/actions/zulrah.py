import mss

from src.actions.action import Action
from src.robot import robot
from src.robot.timer import Timer
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import ControlPanel, Prayer
from src.vision.vision import ContourDetection


class ZulrahAction(Action):
    sct = mss.mss()

    last_zulrah_color = None
    zulrah_color = None
    color_change_tick = 0

    def first_tick(self):
        self.set_progress_message(f'Fighting Zulrah...')

    def tick(self, tick_counter):
        if tick_counter % Timer.sec2tick(1) == 0:
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

            if self.zulrah_color is None and max_color is not None and max_color != self.last_zulrah_color:
                self.color_change_tick = tick_counter
                self.zulrah_color = max_color
                print(max_color, '-->', max_area)
            elif self.zulrah_color is not None and max_color is None:
                self.last_zulrah_color = self.zulrah_color
                self.zulrah_color = None

        # tick_offset = self.color_change_tick
        # if tick_counter == tick_offset:
        #     robot.click(Interface.PRAYER_TAB)
        # tick_offset += Timer.sec2tick(0.5)
        # if tick_counter == tick_offset:
        #     if self.zulrah_color == Color.GREEN:
        #         robot.click(Prayer.PROTECT_FROM_MISSILES)
        #     elif self.zulrah_color == Color.BLUE:
        #         robot.click(Prayer.PROTECT_FROM_MAGIC)
        #     elif self.zulrah_color == Color.RED:
        #         robot.click(Prayer.PROTECT_FROM_MELEE)
        # tick_offset += Timer.sec2tick(1)
        # if tick_counter == tick_offset:
        #     robot.click(Interface.INVENTORY_TAB)

        tick_offset = self.color_change_tick
        if tick_counter == tick_offset:
            robot.press('1')  # prayer tab
        tick_offset += Timer.sec2tick(0.1)
        if tick_counter == tick_offset:
            if self.zulrah_color == Color.GREEN:
                robot.click(Prayer.PROTECT_FROM_MISSILES)
            elif self.zulrah_color == Color.BLUE:
                robot.click(Prayer.PROTECT_FROM_MAGIC)
            elif self.zulrah_color == Color.RED:
                if self.last_zulrah_color == Color.GREEN:
                    robot.click(Prayer.PROTECT_FROM_MISSILES)
                elif self.last_zulrah_color == Color.BLUE:
                    robot.click(Prayer.PROTECT_FROM_MAGIC)
        tick_offset += Timer.sec2tick(0.1)
        if tick_counter == tick_offset:
            robot.press('space')  # inventory tab

        return Action.Status.IN_PROGRESS

    def last_tick(self):
        self.last_zulrah_color = None
        self.zulrah_color = None
        self.color_change_tick = 0
