import cv2 as cv
import numpy as np
from src.vision import vision

haystack = cv.imread('../resources/experiments/screenshot/slayer/abyssal.png', cv.IMREAD_UNCHANGED)
needle = cv.imread('../resources/target/item/shark.png', cv.IMREAD_UNCHANGED)
loc = vision.locate_image(haystack, needle, 0.9)

if loc is not None:
    x, y = round(loc[0]), round(loc[1])
    cv.rectangle(haystack, (x - 5, y - 5), (x + 5, y + 5), color=(0, 255, 0), thickness=-1, lineType=cv.LINE_AA)

cv.imshow('haystack', haystack)
cv.waitKey(0)
