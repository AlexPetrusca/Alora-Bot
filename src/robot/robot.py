import pyautogui
from src.vision import vision
from src.vision.images import Images, Food
from src.vision.regions import Regions
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
    ate_food = click_image(Food.MONKFISH, 0.9, region=Regions.CONTROL_PANEL)
    if not ate_food:
        ate_food = click_image(Food.SHARK, 0.9, region=Regions.CONTROL_PANEL)
    if not ate_food:
        ate_food = click_image(Food.MANTA_RAY, 0.9, region=Regions.CONTROL_PANEL)
    return ate_food


def click_image(image, threshold=0.7, region=Regions.SCREEN):
    loc = vision.locate_image(vision.grab_screen()[region.as_slice()], image, threshold)
    if loc is None:
        return False
    else:
        x, y = region.global_px(loc[0], loc[1])
        click(x / 2, y / 2)
        return True


def click_contour(color, area_threshold=750, mode=ContourDetection.DISTANCE_CLOSEST):
    loc = vision.locate_contour(vision.grab_screen(), color, area_threshold, mode)
    if loc is None:
        return False
    else:
        click(loc[0] / 2, loc[1] / 2)
        return True


def type_text(text):
    pyautogui.press([c for c in text])


def press(key):
    pyautogui.press(key)


def key_down(key):
    pyautogui.keyDown(key)


def key_up(key):
    pyautogui.keyUp(key)
