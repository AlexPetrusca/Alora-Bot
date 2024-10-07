import cv2 as cv

from src.vision.color import Color, get_color_limits

haystack_img = cv.imread('../screenshots/breadcrumb_labels.png', cv.IMREAD_UNCHANGED)
needle_img = cv.imread('../../resources/label/marker/yellow/3.png', cv.IMREAD_UNCHANGED)
haystack_hsv = cv.cvtColor(haystack_img, cv.COLOR_BGR2HSV)

result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

yellow_lower, yellow_upper = get_color_limits(Color.YELLOW.value)
yellow_mask = cv.inRange(haystack_hsv, yellow_lower, yellow_upper)

print('found', '-', max_val)

needle_w = needle_img.shape[1]
needle_h = needle_img.shape[0]

top_left = max_loc
bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

cv.rectangle(haystack_img, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

cv.imshow('Screenshot', haystack_img)
cv.imshow('Yellow Mask', yellow_mask)
cv.waitKey()
