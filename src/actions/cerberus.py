import cv2 as cv
import mss
from pytesseract import pytesseract

from src.actions.action import Action
from src.robot import robot
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import ControlPanel, Prayer, Minimap, ArceuusSpellbook, CerberusActionCoord


class CerberusAction(Action):
    sct = mss.mss()

    tile_color = None
    last_chat = None
    fight_over_tick = None
    retry_count = 0

    def __init__(self):
        pass

    def first_tick(self):
        self.set_status('Routing to Cerberus...')
        pass

    def tick(self, t):
        tick_offset = 0

        # 1. Click 850, 50 + wait to walk
        if self.tick_counter == tick_offset:
            robot.click(CerberusActionCoord.WALK1)

        # 2. Click 750, 90 + wait to walk + wait to enter chamber
        tick_offset += Action.sec2tick(7)
        if self.tick_counter == tick_offset:
            robot.click(CerberusActionCoord.WALK2)

        # 3. Click 850, 215 + wait to walk
        tick_offset += Action.sec2tick(14)
        if self.tick_counter == tick_offset:
            robot.click(CerberusActionCoord.WALK3)

        # 4. Enable prayers + spec
        tick_offset += Action.sec2tick(1)
        if self.tick_counter == tick_offset:
            robot.click(ControlPanel.PRAYER_TAB)
        tick_offset += Action.sec2tick(1)
        if self.tick_counter == tick_offset:
            robot.click(Prayer.PROTECT_FROM_MAGIC)
        tick_offset += Action.sec2tick(1)
        if self.tick_counter == tick_offset:
            robot.click(Prayer.PIETY)
        tick_offset += Action.sec2tick(1)
        if self.tick_counter == tick_offset:
            robot.click(Minimap.SPECIAL)

        # 5. click magenta contour + wait to start fight
        tick_offset += Action.sec2tick(1)
        if self.tick_counter == tick_offset:
            self.tile_color = Color.MAGENTA
            robot.click_contour(self.tile_color)

        # 6. summon thrall
        tick_offset += Action.sec2tick(3)
        if self.tick_counter == tick_offset:
            self.set_status('Fighting Cerberus...')
            robot.click(ControlPanel.MAGIC_TAB)
        tick_offset += Action.sec2tick(1)
        if self.tick_counter == tick_offset:
            robot.click(ArceuusSpellbook.RESURRECT_GREATER_SKELETON)
        tick_offset += Action.sec2tick(1)
        if self.tick_counter == tick_offset:
            robot.click(ControlPanel.INVENTORY_TAB)

        # 7. Wait for fight end + on "Grrrr", click yellow contour + on low health, eat
        if self.tick_counter > tick_offset and self.fight_over_tick is None:
            if self.tick_counter % Action.sec2tick(1) == 0:
                damage_ui = vision.grab_damage_ui(self.sct)
                ocr = pytesseract.image_to_string(damage_ui).strip()  # todo: move ocr to vision module
                if ocr.startswith('0/'):
                    self.fight_over_tick = self.tick_counter
                elif ocr.find("/") == -1:  # "/" not found
                    self.retry_count += 1
                    if self.retry_count > 5:
                        return True

                if vision.read_hitpoints(self.sct) <= 30:
                    robot.click_food()

            if self.tick_counter % Action.sec2tick(0.5) == 0:
                chat = vision.read_latest_chat(self.sct)
                # print(chat, "->", chat.find("Cerberus: Grr"))
                if chat.find("Cerberus: Grr") == 0 and chat != self.last_chat:
                    # print("HIT ------------>", chat)
                    self.tile_color = Color.YELLOW if self.tile_color == Color.MAGENTA else Color.MAGENTA
                    robot.click_contour(self.tile_color)
                    robot.press(['Enter', 'h', 'a', 'h', 'a', 'Enter'])
                self.last_chat = chat

        if self.fight_over_tick is not None:
            tick_offset = self.fight_over_tick

            # 8. Disable prayers
            tick_offset += Action.sec2tick(1)
            if self.tick_counter == tick_offset:
                robot.click(ControlPanel.PRAYER_TAB)
            tick_offset += Action.sec2tick(1)
            if self.tick_counter == tick_offset:
                robot.click(Prayer.PROTECT_FROM_MAGIC)
            tick_offset += Action.sec2tick(1)
            if self.tick_counter == tick_offset:
                robot.click(Prayer.PIETY)

            # 9. End fight
            tick_offset += Action.sec2tick(2)
            if self.tick_counter == tick_offset:
                return True

        return False

    def last_tick(self):
        self.tile_color = None
        self.last_chat = None
        self.fight_over_tick = None
        self.retry_count = 0
