from pytesseract import pytesseract

from src.vision import vision


def latest_chat(sct):
    chat_line_image = vision.grab_screen(sct)[2106:2144, 14:994]
    return pytesseract.image_to_string(chat_line_image)
