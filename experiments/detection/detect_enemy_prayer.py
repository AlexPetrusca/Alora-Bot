from time import perf_counter

import cv2 as cv
import numpy as np

from src.robot.timing.timer import Timer
from src.vision import vision
from src.vision.color import Color
from src.vision.coordinates import Player
from src.vision.regions import Regions

# haystack = cv.imread('../screenshots/enemy_prayer/demonic_gorillas_2.png', cv.IMREAD_UNCHANGED)
haystack = cv.imread('../screenshots/enemy_prayer/tormented_demon_2.png', cv.IMREAD_UNCHANGED)
# haystack = cv.imread('../screenshots/hazards/hazard2.png', cv.IMREAD_UNCHANGED)
# haystack = cv.imread('../screenshots/ground_items/ground_items_4.png', cv.IMREAD_UNCHANGED)
# haystack = cv.imread('../screenshots/antibot/racecar.png', cv.IMREAD_UNCHANGED)

melee_prayer = cv.imread('../../resources/prayer/melee.png', cv.IMREAD_UNCHANGED)
magic_prayer = cv.imread('../../resources/prayer/magic.png', cv.IMREAD_UNCHANGED)
ranged_prayer = cv.imread('../../resources/prayer/ranged.png', cv.IMREAD_UNCHANGED)


def time(fn, label=""):
    t = perf_counter()
    status = fn()
    d = perf_counter() - t
    print(f'{label}: {d / Timer.TICK_INTERVAL} ticks')
    return status


def locate_opponent(haystack):
    contour, _ = vision.get_contour(haystack, Color.RED)
    x, y, w, h = cv.boundingRect(contour)
    return x, y - 75, w, h + 75


def locate_my_prayer(haystack):
    return vision.get_prayer_protect(haystack[Regions.PLAYER.as_slice()])


def locate_opponent_prayer(haystack):
    x, y, w, h = locate_opponent(haystack)
    return vision.get_prayer_protect(haystack[y:(y + h), x:(x + w)])


player_detect = np.copy(haystack)
px, py = 2 * Player.POSITION.value[0], 2 * Player.POSITION.value[1]
cv.rectangle(player_detect, (px - 5, py - 5), (px + 5, py + 5), color=(0, 255, 0), thickness=-1, lineType=cv.LINE_AA)
x, y, w, h = 2 * Regions.PLAYER.x, 2 * Regions.PLAYER.y, 2 * Regions.PLAYER.w, 2 * Regions.PLAYER.h
cv.rectangle(player_detect, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)
cv.imshow('Player', player_detect)

enemy_detect = np.copy(haystack)
x, y, w, h = locate_opponent(enemy_detect)
cv.rectangle(enemy_detect, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)
cv.imshow('Enemy', enemy_detect)

my_prayer_detect = np.copy(haystack)
my_prayer, my_prayer_loc = locate_my_prayer(my_prayer_detect)
if my_prayer_loc is not None:
    x, y = 2 * Regions.PLAYER.x + my_prayer_loc[0], 2 * Regions.PLAYER.y + my_prayer_loc[1]
    cv.rectangle(my_prayer_detect, (int(x) - 5, int(y) - 5), (int(x) + 5, int(y) + 5), color=(0, 255, 0), thickness=-1)
    cv.imshow('My Prayer', my_prayer_detect)
    print("My Prayer", my_prayer)
else:
    print("Couldn't find my prayer")

opp_prayer_detect = np.copy(haystack)
opp_prayer, opp_prayer_loc = locate_opponent_prayer(opp_prayer_detect)
if opp_prayer_loc is not None:
    sx, sy, _, _ = locate_opponent(haystack)
    x, y = sx + opp_prayer_loc[0], sy + opp_prayer_loc[1]
    cv.rectangle(opp_prayer_detect, (int(x) - 5, int(y) - 5), (int(x) + 5, int(y) + 5), color=(0, 255, 0), thickness=-1)
    cv.imshow('Opponent Prayer', opp_prayer_detect)
    print("Opponent Prayer", opp_prayer)
else:
    print("Couldn't find opponent prayer")

cv.waitKey(0)
