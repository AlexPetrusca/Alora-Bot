import cv2 as cv
import numpy as np

haystack = cv.imread('../screenshots/grimy_bank.png', cv.IMREAD_UNCHANGED)
needle = cv.imread('../../resources/item/herblore/grimy_herb/grimy_dwarf_weed.png', cv.IMREAD_UNCHANGED)

y_start = needle.shape[0] // 4
y_end = needle.shape[0]
needle = needle[y_start:y_end, 0:needle.shape[1]]

res = cv.matchTemplate(haystack, needle, cv.TM_CCOEFF_NORMED)
points = list(zip(*np.where(res > 0.95)))

for point in points:
    print(point, '-->', res[point])

    y, x = point[0] + needle.shape[0] // 2, point[1] + needle.shape[1] // 2
    cv.rectangle(haystack, (x - 5, y - 5), (x + 5, y + 5), color=(0, 255, 0), thickness=-1, lineType=cv.LINE_AA)

cv.imshow('haystack', haystack)
cv.imshow('needle', needle)
cv.waitKey(0)
