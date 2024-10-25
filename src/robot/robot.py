import pyautogui
from src.vision import vision
from src.vision.images import Images, Food
from src.vision.regions import Regions
from src.vision.vision import ContourDetection


def click(x, y=None):
    if x is None:
        return

    if isinstance(x, tuple):
        pyautogui.moveTo(x)
    elif hasattr(x, 'value'):
        pyautogui.moveTo(x.value)
    else:
        pyautogui.moveTo(x, y)
    pyautogui.click()


def right_click(x, y=None):
    if x is None:
        return

    if isinstance(x, tuple):
        pyautogui.moveTo(x)
    elif hasattr(x, 'value'):
        pyautogui.moveTo(x.value)
    else:
        pyautogui.moveTo(x, y)
    pyautogui.rightClick()


def shift_click(x, y=None):
    with pyautogui.hold('shift'):
        click(x, y)


def click_food():
    ate_food = click_image(Food.MONKFISH, 0.99, region=Regions.CONTROL_PANEL, silent=True)
    if not ate_food:
        ate_food = click_image(Food.SHARK, 0.99, region=Regions.CONTROL_PANEL, silent=True)
    if not ate_food:
        ate_food = click_image(Food.MANTA_RAY, 0.99, region=Regions.CONTROL_PANEL, silent=True)
    return ate_food


def click_potion(potion):
    drank_potion = click_image(potion.doses[1], 0.99, region=Regions.INVENTORY, silent=True)
    if not drank_potion:
        drank_potion = click_image(potion.doses[2], 0.99, region=Regions.INVENTORY, silent=True)
    if not drank_potion:
        drank_potion = click_image(potion.doses[3], 0.99, region=Regions.INVENTORY, silent=True)
    if not drank_potion:
        drank_potion = click_image(potion.doses[4], 0.99, region=Regions.INVENTORY, silent=True)
    return drank_potion


def click_image(image, threshold=0.7, region=Regions.SCREEN, half_scale=False, silent=False):
    screen = vision.grab_screen()
    if region == Regions.SCREEN:
        loc = vision.locate_image(screen, image, threshold, half_scale=half_scale, silent=silent)
    else:
        loc = vision.locate_image(screen[region.as_slice()], image, threshold, half_scale=half_scale, silent=silent)

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
    pyautogui.typewrite(text)


def press(key):
    pyautogui.press(key)


def key_down(key):
    pyautogui.keyDown(key)


def key_up(key):
    pyautogui.keyUp(key)


def hold_key(key, t):
    with pyautogui.hold(key):
        pyautogui.sleep(t)
