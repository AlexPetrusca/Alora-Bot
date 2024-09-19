import mss
import pyautogui

from src.util import vision


def click(x=None, y=None):
    if isinstance(x, tuple):
        pyautogui.moveTo(x)
    else:
        pyautogui.moveTo(x, y)
    pyautogui.click()

def right_click(x=None, y=None):
    if isinstance(x, tuple):
        pyautogui.moveTo(x)
    else:
        pyautogui.moveTo(x, y)
    pyautogui.rightClick()

def shift_click(x, y):
    with pyautogui.hold('shift'):
        click(x, y)

def click_image(image):
    screenshot = vision.grab_screen(mss.mss())  # todo: can we avoid reinitializing mss each time
    x, y = vision.locate_image(screenshot, image)  # todo: this blows up if the image isn't found
    click(x / 2, y / 2)


def click_outline(color):
    screenshot = vision.grab_screen(mss.mss())  # todo: can we avoid reinitializing mss each time
    x, y = vision.locate_outline(screenshot, color)
    click(x / 2, y / 2)

def press(key):
    pyautogui.press(key)


def key_down(key):
    pyautogui.keyDown(key)


def key_up(key):
    pyautogui.keyUp(key)
