import cv2 as cv
import mss
from pytesseract import pytesseract

from src.actions.action import Action
from src.util import robot
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import Controls, Prayer, Minimap, ArceuusSpellbook


# 1. Click 850, 50 + wait to walk
# 2. Click 750, 90 + wait to walk + wait to enter chamber
# 3. Click 850, 215 + wait to walk + enable prayers
# 4. Click yellow contour + spec + wait to walk + summon thrall
# 5. Wait for fight end + on "Grrrr", click yellow contour + on low health, eat
# 6. Disable prayers

class CerberusAction(Action):
    sct = mss.mss()

    fight_over_tick = None
    last_chat = None

    def __init__(self):
        pass

    def first_tick(self):
        self.set_status('Routing to Cerberus...')
        pass

    def tick(self, t):
        tick_offset = 0

        # 1. Click 850, 50 + wait to walk
        if self.tick_counter == tick_offset:
            robot.click(850, 50)

        # 2. Click 750, 90 + wait to walk + wait to enter chamber
        tick_offset += Action.sec2tick(7)
        if self.tick_counter == tick_offset:
            robot.click(750, 90)

        # 3. Click 850, 215 + wait to walk
        tick_offset += Action.sec2tick(14)
        if self.tick_counter == tick_offset:
            robot.click(850, 215)

        # 4. Enable prayers + spec
        tick_offset += Action.sec2tick(5)
        if self.tick_counter == tick_offset:
            robot.click(Controls.PRAYER_TAB.value)
        tick_offset += Action.sec2tick(1)
        if self.tick_counter == tick_offset:
            robot.click(Prayer.PROTECT_FROM_MAGIC.value)
        tick_offset += Action.sec2tick(1)
        if self.tick_counter == tick_offset:
            robot.click(Prayer.PIETY.value)
        tick_offset += Action.sec2tick(1)
        if self.tick_counter == tick_offset:
            robot.click(Minimap.SPECIAL.value)

        # 5. click yellow contour + wait to start fight
        tick_offset += Action.sec2tick(1)
        if self.tick_counter == tick_offset:
            robot.click_contour(Color.YELLOW.value)

        # 6. summon thrall
        tick_offset += Action.sec2tick(3)
        if self.tick_counter == tick_offset:
            robot.click(Controls.MAGIC_TAB.value)
        tick_offset += Action.sec2tick(1)
        if self.tick_counter == tick_offset:
            robot.click(ArceuusSpellbook.RESURRECT_GREATER_SKELETON.value)

        # 7. Wait for fight end + on "Grrrr", click yellow contour + on low health, eat
        if self.tick_counter > tick_offset and self.fight_over_tick is None:
            if self.tick_counter % Action.sec2tick(1) == 0:
                damage_ui = vision.grab_damage_ui(self.sct)
                ocr = pytesseract.image_to_string(damage_ui).strip()  # todo: move ocr to vision module
                if ocr.startswith('0/'):
                    self.fight_over_tick = self.tick_counter

                chat = vision.get_latest_chat(self.sct).strip()
                print(chat, "->", chat.find("Cerberus: Grr"))
                if chat.find("Cerberus: Grr") == 0 and chat != self.last_chat:
                    print("HIT ------------>", chat)
                    robot.click_contour(Color.YELLOW.value)
                self.last_chat = chat

        if self.fight_over_tick is not None:
            tick_offset = self.fight_over_tick

            # 8. Disable prayers
            tick_offset += Action.sec2tick(1)
            if self.tick_counter == tick_offset:
                robot.click(Controls.PRAYER_TAB.value)
            tick_offset += Action.sec2tick(1)
            if self.tick_counter == tick_offset:
                robot.click(Prayer.PROTECT_FROM_MAGIC.value)
            tick_offset += Action.sec2tick(1)
            if self.tick_counter == tick_offset:
                robot.click(Prayer.PIETY.value)
                return True

        return False

    def last_tick(self):
        self.fight_over_tick = None
        self.last_chat = None
