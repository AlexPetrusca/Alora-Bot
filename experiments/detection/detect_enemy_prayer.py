from time import perf_counter

import cv2 as cv
import numpy as np

from src.robot.timing.timer import Timer
from src.vision import vision
from src.vision.color import Color
from src.vision.images import PrayerProtect
from src.vision.regions import Regions

# haystack = cv.imread('../screenshots/enemy_prayer/demonic_gorillas_2.png', cv.IMREAD_UNCHANGED)
haystack = cv.imread('../screenshots/enemy_prayer/tormented_demon_2.png', cv.IMREAD_UNCHANGED)
# haystack = cv.imread('../screenshots/hazards/hazard2.png', cv.IMREAD_UNCHANGED)
# haystack = cv.imread('../screenshots/ground_items/ground_items_4.png', cv.IMREAD_UNCHANGED)
# haystack = cv.imread('../screenshots/antibot/racecar.png', cv.IMREAD_UNCHANGED)

melee_prayer = cv.imread('../../resources/prayer/melee.png', cv.IMREAD_UNCHANGED)
magic_prayer = cv.imread('../../resources/prayer/magic.png', cv.IMREAD_UNCHANGED)
ranged_prayer = cv.imread('../../resources/prayer/ranged.png', cv.IMREAD_UNCHANGED)


def locate_image(haystack, needle):
    locate_image = np.copy(haystack)

    loc = vision.locate_image(locate_image, needle, 0.9)
    if loc is not None:
        x, y = round(loc[0]), round(loc[1])
        cv.rectangle(locate_image, (x - 5, y - 5), (x + 5, y + 5), color=(0, 255, 0), thickness=-1, lineType=cv.LINE_AA)

        top_left = (x - needle.shape[1] // 2, y - needle.shape[0] // 2)
        bottom_right = (x + needle.shape[1] // 2, y + needle.shape[0] // 2)
        cv.rectangle(locate_image, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

    return locate_image


def locate_player(haystack):
    player_detect = np.copy(haystack)

    player_x, player_y = Regions.GAME.w // 2 - 10, Regions.GAME.y + Regions.GAME.h // 2 - 20
    # player_w, player_h = 50, 100
    player_w, player_h = 75, 100
    top_left = (player_x - player_w // 2, player_y - player_h // 2)
    bottom_right = (player_x + player_w // 2, player_y + player_h // 2)

    vision.mask_player(player_detect)

    screen_player_x, screen_player_y = 2 * player_x, 2 * player_y
    cv.rectangle(player_detect, (screen_player_x - 5, screen_player_y - 5), (screen_player_x + 5, screen_player_y + 5), color=(0, 255, 0), thickness=-1, lineType=cv.LINE_AA)

    screen_top_left = (2 * top_left[0], 2 * top_left[1])
    screen_bottom_right = (2 * bottom_right[0], 2 * bottom_right[1])
    cv.rectangle(player_detect, screen_top_left, screen_bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

    return player_detect


def locate_my_prayer(haystack):
    return_image = np.copy(haystack)

    player_img = haystack[Regions.PLAYER.as_slice()]

    melee_loc = vision.locate_image(player_img, melee_prayer, 0.9)
    if melee_loc is not None:
        return return_image

    magic_loc = vision.locate_image(player_img, magic_prayer, 0.9)
    if magic_loc is not None:
        return return_image

    ranged_loc = vision.locate_image(player_img, ranged_prayer, 0.9)
    if ranged_loc is not None:
        return return_image

    return return_image


def locate_enemy_prayer(haystack):
    pass


cv.imshow('Image Detect', locate_image(haystack, ranged_prayer))
cv.imshow('Player Detect', locate_player(haystack))
cv.imshow('My Prayer Detect', locate_my_prayer(haystack))


print('--------------------------------------------------------------------')


t = perf_counter()
result = cv.matchTemplate(haystack, magic_prayer, cv.TM_CCOEFF_NORMED)
d0 = perf_counter() - t
print('cv.matchTemplate:', d0 / Timer.TICK_INTERVAL, 'ticks')
# cv.imshow('Match Template', result)

t = perf_counter()
_, max_val, _, max_loc = cv.minMaxLoc(result)
d1 = perf_counter() - t
print('cv.minMaxLoc:', d1 / Timer.TICK_INTERVAL, 'ticks', '-->', max_loc)

t = perf_counter()
out = np.unravel_index(np.argmax(result), result.shape)
# y, x = out // result.shape[1], out % result.shape[1]
d2 = perf_counter() - t
print('myMaxLoc:', d2 / Timer.TICK_INTERVAL, 'ticks', '-->', out)

print('Ratio:', d2 / d1)

t = perf_counter()
locations = np.where(result >= 0.85)
d3 = perf_counter() - t
print('Locations:', d3 / Timer.TICK_INTERVAL, 'ticks', '-->', locations)


def time(fn, label=""):
    t = perf_counter()
    status = fn()
    d = perf_counter() - t
    print(f'{label}: {d / Timer.TICK_INTERVAL} ticks')
    return status


def findViaContour():
    contour, _ = vision.get_contour(haystack, Color.RED)
    x, y, w, h = cv.boundingRect(contour)
    cv.rectangle(haystack, (x, y - 75), (x + w, y + h), (0, 255, 0), 2)

    enemy_img = haystack[(y - 75):(y + h), x:(x + w)]
    melee_loc = vision.locate_image(enemy_img, melee_prayer, 0.9)
    if melee_loc is not None:
        return PrayerProtect.MELEE, melee_loc
    magic_loc = vision.locate_image(enemy_img, magic_prayer, 0.9)
    if magic_loc is not None:
        return PrayerProtect.MAGIC, magic_loc
    ranged_loc = vision.locate_image(enemy_img, ranged_prayer, 0.9)
    if ranged_loc is not None:
        return PrayerProtect.RANGED, ranged_loc

    return None, None


prayer_protect = time(findViaContour, "findViaContour")
print(prayer_protect)

cv.imshow('HAYSTACK', haystack)

cv.waitKey(0)
