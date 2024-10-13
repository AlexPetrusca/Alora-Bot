import cv2 as cv
from src.vision import vision

haystack = cv.imread('../screenshots/status_bar/fire_resist_3.png', cv.IMREAD_UNCHANGED)
needle = cv.imread('../../resources/status/antifire.png', cv.IMREAD_UNCHANGED)
loc = vision.locate_image(haystack, needle, 0.85)

if loc is not None:
    x, y = round(loc[0]), round(loc[1])
    cv.rectangle(haystack, (x - 5, y - 5), (x + 5, y + 5), color=(0, 255, 0), thickness=-1, lineType=cv.LINE_AA)

    top_left = (x - needle.shape[1] // 2, y - needle.shape[0] // 2)
    bottom_right = (x + needle.shape[1] // 2, y + needle.shape[0] // 2)
    cv.rectangle(haystack, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

cv.imshow('haystack', haystack)
cv.waitKey(0)
