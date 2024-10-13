import cv2 as cv
import numpy as np

from src.vision import vision
from src.vision.color import Color, get_color_limits
from src.vision.vision import ContourDetection


def simple_detection(img):
    img = np.copy(img)
    contour, _ = vision.get_contour(img, Color.MAGENTA, area_threshold=100, mode=ContourDetection.AREA_LARGEST)
    if contour is not None:
        x, y, w, h = cv.boundingRect(contour)
        cv.rectangle(img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)
    else:
        print("WTF")

    cv.imshow('Detection - Simple', img)


def advanced_detection(img):
    img = np.copy(img)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower_limit, upper_limit = get_color_limits(Color.MAGENTA)
    mask = cv.inRange(hsv, lower_limit, upper_limit)
    mask = cv.blur(mask, (5, 5))
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, np.ones((50, 5), np.uint8))
    contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv.contourArea(contour) > 250:
            x, y, w, h = cv.boundingRect(contour)
            cv.rectangle(img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2, lineType=cv.LINE_AA)

    cv.imshow('Detection - Advanced', img)
    cv.imshow('Mask', mask)


haystack = vision.mask_ui(cv.imread('../screenshots/hazards/hazard1.png', cv.IMREAD_UNCHANGED))

simple_detection(haystack)
advanced_detection(haystack)

cv.waitKey()
cv.destroyAllWindows()
