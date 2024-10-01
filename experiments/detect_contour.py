import cv2 as cv

from src.util.common import mask_ui, get_color_limits

COLOR_RED = [0, 0, 255]

haystack = mask_ui(cv.imread('../resources/experiments/screenshot/slayer/nechryael.png', cv.IMREAD_UNCHANGED))
_, threshold = cv.threshold(haystack, 0, 255, cv.THRESH_BINARY)

hsv_threshold = cv.cvtColor(threshold, cv.COLOR_BGR2HSV)
lower_limit, upper_limit = get_color_limits(COLOR_RED)
mask = cv.inRange(hsv_threshold, lower_limit, upper_limit)

contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
if len(contours) > 0:
    for contour in contours:
        if cv.contourArea(contour) > 750:
            x, y, w, h = cv.boundingRect(contour)
            cv.rectangle(haystack, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

cv.imshow('Original', haystack)
cv.imshow('Threshold', threshold)
cv.imshow('Range Mask', mask)
cv.waitKey()
cv.destroyAllWindows()
