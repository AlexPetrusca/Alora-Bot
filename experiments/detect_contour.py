import cv2 as cv

from src.util.common import hide_ui

COLOR_RED = [0, 0, 255]

haystack = hide_ui(cv.imread('../resources/experiments/screenshot/slayer/nechryael.png', cv.IMREAD_UNCHANGED))
needle = cv.imread('../resources/experiments/target/outline.png', cv.IMREAD_UNCHANGED)
_, threshold = cv.threshold(haystack, 0, 255, cv.THRESH_BINARY)

result = cv.matchTemplate(threshold, needle, cv.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
print('found', '-', max_val)

needle_w = needle.shape[1]
needle_h = needle.shape[0]
top_left = max_loc
bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
cv.rectangle(haystack, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

cv.imshow('Original', haystack)
cv.imshow('Threshold', threshold)
cv.waitKey()
cv.destroyAllWindows()
