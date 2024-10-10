from src.actions.primitives.action import Action
from src.robot import robot
from src.robot.timer import Timer
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import Prayer, ControlPanel
from src.vision.vision import ContourDetection


class ZulrahAction(Action):
    def __init__(self):
        super().__init__()
        self.last_zulrah_color = None
        self.zulrah_color = None
        self.color_change_tick = 0

    def first_tick(self):
        self.set_progress_message(f'Fighting Zulrah...')

    def tick(self, timing):
        timing.interval(Timer.sec2tick(1), lambda: self.detect_color_change(timing))

        timing.tick_offset = self.color_change_tick

        # # Slow prayer change
        # timing.execute(lambda: robot.click(ControlPanel.PRAYER_TAB))  # prayer tab
        # timing.execute_after(Timer.sec2tick(0.5), self.protect_against_color)
        # timing.execute_after(Timer.sec2tick(0.5), lambda: robot.click(ControlPanel.INVENTORY_TAB))  # inventory tab

        # Fast prayer change
        timing.execute(lambda: robot.press('1'))  # prayer tab
        timing.execute_after(Timer.sec2tick(0.1), self.protect_against_color)
        timing.execute_after(Timer.sec2tick(0.1), lambda: robot.press('space'))  # inventory tab

        return Action.Status.IN_PROGRESS

    def protect_against_color(self):
        if self.zulrah_color == Color.GREEN:
            robot.click(Prayer.PROTECT_FROM_MISSILES)
        elif self.zulrah_color == Color.BLUE:
            robot.click(Prayer.PROTECT_FROM_MAGIC)
        elif self.zulrah_color == Color.RED:
            if self.last_zulrah_color == Color.GREEN:
                robot.click(Prayer.PROTECT_FROM_MISSILES)
            elif self.last_zulrah_color == Color.BLUE:
                robot.click(Prayer.PROTECT_FROM_MAGIC)

    def detect_color_change(self, timing):
        screenshot = vision.grab_screen(hide_ui=True)
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
            self.color_change_tick = timing.tick_counter
            self.zulrah_color = max_color
            print(max_color, '-->', max_area)
        elif self.zulrah_color is not None and max_color is None:
            self.last_zulrah_color = self.zulrah_color
            self.zulrah_color = None

    def last_tick(self):
        self.last_zulrah_color = None
        self.zulrah_color = None
        self.color_change_tick = 0
