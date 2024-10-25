from src.actions.combat.combat import CombatAction
from src.actions.prayer import PrayerAction
from src.robot import robot
from src.robot.timing.timer import Timer
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import Prayer, ArceuusSpellbook
from src.vision.images import Potion
from src.vision.vision import ContourDetection


# Requirements
#   - Turn on "Entity Hider" > "Hide NPCs 2D"
class ZulrahAction(CombatAction):
    def __init__(self):
        super().__init__(target=None, health_threshold=75, sip_prayer=True, cure_poison=True,
                         potions=[Potion.RANGING], thrall=ArceuusSpellbook.RESURRECT_GREATER_SKELETON)

        self.prayer_action = PrayerAction(switch_to_inventory=True)

    def first_tick(self):
        self.set_progress_message('Fighting Zulrah...')

    def tick(self, timing):
        timing.observe(Timer.sec2tick(1), self.track_color, self.respond_to_color_change)
        return super().tick(timing)

    def track_color(self):
        screenshot = vision.grab_screen(hide_ui=True)
        red_contour, red_area = vision.get_contour(screenshot, Color.RED, mode=ContourDetection.AREA_LARGEST)
        green_contour, green_area = vision.get_contour(screenshot, Color.GREEN, mode=ContourDetection.AREA_LARGEST)
        blue_contour, blue_area = vision.get_contour(screenshot, Color.BLUE, mode=ContourDetection.AREA_LARGEST)

        max_area, max_color = 100, None
        if red_area > max_area:
            max_area, max_color = red_area, Color.RED
        if green_area > max_area:
            max_area, max_color = green_area, Color.GREEN
        if blue_area > max_area:
            max_area, max_color = blue_area, Color.BLUE

        self.target = max_color
        if self.target == Color.GREEN:
            self.prayer_action.set_prayers(Prayer.PROTECT_FROM_MISSILES)
        elif self.target == Color.BLUE:
            self.prayer_action.set_prayers(Prayer.PROTECT_FROM_MAGIC)
        else:
            self.prayer_action.disable_all_prayers()

        return self.target

    def respond_to_color_change(self, timing, from_status, to_status):
        timing.execute(lambda: print("ZULRAH CHANGE:", from_status, "-->", to_status))
        timing.action(self.prayer_action)
        if self.target is not None:
            timing.execute(lambda: robot.click_contour(self.target))

    def last_tick(self):
        super().last_tick()
