import cv2 as cv
import numpy as np
from src.util.common import hide_ui, get_color_limits
from src.vision import vision
from src.vision.color import Color

screenshot_image = cv.imread('../resources/experiments/screenshot/edgeville.png', cv.IMREAD_UNCHANGED)


screenshot_threshold = cv.cvtColor(screenshot_image, cv.COLOR_BGR2HSV)
lower_limit, upper_limit = get_color_limits(Color.WHITE.value)
mask = cv.inRange(screenshot_threshold, lower_limit, upper_limit)
cv.imshow("Mask", mask)

kernel = np.ones((10, 200), np.uint8)
morph = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
cv.imshow("Morphology", morph)

tx, ty = vision.locate_ground_item(screenshot_image)
cv.rectangle(screenshot_image, (tx - 5, ty - 5), (tx + 5, ty + 5), color=(0, 0, 255), thickness=-1, lineType=cv.LINE_4)

contours, _ = cv.findContours(morph, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
if len(contours) > 0:
    for contour in contours:
        if cv.contourArea(contour) > 750:
            x, y, w, h = cv.boundingRect(contour)
            cv.rectangle(screenshot_image, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

cv.imshow("Screenshot", screenshot_image)
cv.waitKey(0)
