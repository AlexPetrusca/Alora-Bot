import mss
import pyautogui
import cv2 as cv
from src.vision import vision
from src.vision.vision import ContourDetection


def click(x=None, y=None):
    if isinstance(x, tuple):
        pyautogui.moveTo(x)
    elif hasattr(x, 'value'):
        pyautogui.moveTo(x.value)
    else:
        pyautogui.moveTo(x, y)
    pyautogui.click()


def right_click(x=None, y=None):
    if isinstance(x, tuple):
        pyautogui.moveTo(x)
    elif hasattr(x, 'value'):
        pyautogui.moveTo(x.value)
    else:
        pyautogui.moveTo(x, y)
    pyautogui.rightClick()


def shift_click(x=None, y=None):
    with pyautogui.hold('shift'):
        click(x, y)


def click_food():
    ate_food = click_image(cv.imread('../resources/target/item/monkfish.png', cv.IMREAD_UNCHANGED), 0.9)
    if not ate_food:
        ate_food = click_image(cv.imread('../resources/target/item/shark.png', cv.IMREAD_UNCHANGED), 0.9)
    if not ate_food:
        ate_food = click_image(cv.imread('../resources/target/item/manta_ray.png', cv.IMREAD_UNCHANGED), 0.9)
    return ate_food


def click_image(image, threshold=0.7):
    screenshot = vision.grab_screen(mss.mss())  # todo: can we avoid reinitializing mss each time
    loc = vision.locate_image(screenshot, image, threshold)
    if loc is None:
        return False
    else:
        click(loc[0] / 2, loc[1] / 2)
        return True


def click_contour(color, area_threshold=750, mode=ContourDetection.DISTANCE_CLOSEST):
    screenshot = vision.grab_screen(mss.mss())  # todo: can we avoid reinitializing mss each time
    loc = vision.locate_contour(screenshot, color, area_threshold, mode)
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
