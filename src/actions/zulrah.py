from src.actions.prayer import PrayerAction
from src.actions.primitives.action import Action
from src.actions.types.action_status import ActionStatus
from src.robot.timing.timer import Timer
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import Prayer
from src.vision.vision import ContourDetection


# Requirements
#   - Turn on "Entity Hider" > "Hide NPCs 2D"
class ZulrahAction(Action):
    def __init__(self):
        super().__init__()
        self.last_zulrah_color = None
        self.zulrah_color = None

        self.prayer_action = PrayerAction(switch_inventory=True)

    def first_tick(self):
        self.set_progress_message('Fighting Zulrah...')

    def tick(self, timing):
        timing.observe(Timer.sec2tick(1), self.track_color, self.respond_to_color_change)
        return ActionStatus.IN_PROGRESS

    def respond_to_color_change(self, timing, from_status, to_status):
        timing.action(self.prayer_action)

    def track_color(self):
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
            self.zulrah_color = max_color
            self.prayer_action.set_prayer(self.protect_against_color())
            1 
        elif self.zulrah_color is not None and max_color is None:
            self.last_zulrah_color = self.zulrah_color
            self.zulrah_color = None
            self.prayer_action.disable_all_prayers()
        return self.zulrah_color

    def protect_against_color(self):
        if self.zulrah_color == Color.GREEN:
            return Prayer.PROTECT_FROM_MISSILES
        elif self.zulrah_color == Color.BLUE:
            return Prayer.PROTECT_FROM_MAGIC

    def last_tick(self):
        self.last_zulrah_color = None
        self.zulrah_color = None
