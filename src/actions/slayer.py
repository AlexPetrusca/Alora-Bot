import cv2 as cv
import mss
from pytesseract import pytesseract

from src.actions.action import Action
from src.util import vision, robot
from src.util.color import Color


class SlayerAction(Action):
    sct = mss.mss()
    color = Color.RED.value

    fight_over_tick = None
    retry_count = 0

    def __init__(self, color=Color.RED.value):
        self.color = color

    def first_tick(self):
        pass

    def tick(self, t):
        if self.tick_counter == 0:
            print("DO_CLICK")
            robot.click_outline(self.color)
        elif self.tick_counter > Action.sec2tick(4) and self.fight_over_tick is None:
            if self.tick_counter % Action.sec2tick(1) == 0:
                damage_ui = vision.grab_damage_ui(mss.mss())
                ocr = pytesseract.image_to_string(damage_ui).strip()
                print('"', ocr, '"', len(ocr))
                if ocr.startswith("0/"):
                    self.fight_over_tick = self.tick_counter
                elif ocr.find("/") == -1:  # "/" not found
                    self.retry_count += 1
                    if self.retry_count > 3:
                        self.fight_over_tick = self.tick_counter

        if self.fight_over_tick is not None:
            return self.tick_counter > self.fight_over_tick + Action.sec2tick(2)
        else:
            return False

    def last_tick(self):
        self.fight_over_tick = None
        self.retry_count = 0
