import mss
import pyautogui

from src.vision import vision


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


def click_image(image, threshold=0.7):
    screenshot = vision.grab_screen(mss.mss())  # todo: can we avoid reinitializing mss each time
    loc = vision.locate_image(screenshot, image, threshold)
    if loc is None:
        return False
    else:
        click(loc[0] / 2, loc[1] / 2)
        return True


def click_contour(color):
    screenshot = vision.grab_screen(mss.mss())  # todo: can we avoid reinitializing mss each time
    loc = vision.locate_contour(screenshot, color)
    if loc is None:
        return False
    else:
        click(loc[0] / 2, loc[1] / 2)
        return True


def press(key):
    pyautogui.press(key)


def key_down(key):
    pyautogui.keyDown(key)


def key_up(key):
    pyautogui.keyUp(key)
