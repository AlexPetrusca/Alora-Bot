import cv2 as cv

from src.vision.color import Color
from src.vision.coordinates import Prayer
from src.vision import vision
from src.vision.regions import Regions

# haystack = cv.imread('../screenshots/prayer_toggles/piety_protect_melee.png', cv.IMREAD_UNCHANGED)
haystack = cv.imread('../screenshots/prayer_toggles/retribution_protect_item.png', cv.IMREAD_UNCHANGED)


def cutout_prayer(prayer):
    region = Regions.PRAYER(prayer)
    subimage = haystack[region.as_slice()]

    x, y = region.w, 1
    score_on = Color.PRAYER_TOGGLE_ON.distance(subimage[y][x])
    score_off = Color.PRAYER_TOGGLE_OFF.distance(subimage[y][x])
    min_score = min(score_on, score_off)
    print(str(prayer), ":", 'ON' if (min_score == score_on) else 'OFF')

    cv.rectangle(subimage, (x, y), (x + 1, y + 1), color=(0, 255, 0), thickness=-1, lineType=cv.LINE_AA)
    cv.imshow(str(prayer), subimage)


cutout_prayer(Prayer.PIETY)
cutout_prayer(Prayer.PROTECT_FROM_MELEE)

cutout_prayer(Prayer.RETRIBUTION)
cutout_prayer(Prayer.PROTECT_ITEM)

# cv.imshow('haystack', haystack)
cv.waitKey(0)
