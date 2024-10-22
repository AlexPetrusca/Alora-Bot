import cv2 as cv
import numpy as np

from src.vision.regions import Regions

haystack_img = cv.imread('../screenshots/control_panel_bars/prayer_on.png', cv.IMREAD_UNCHANGED)
prayer_off_img = cv.imread('../screenshots/control_panel_bars/prayer_off.png', cv.IMREAD_UNCHANGED)
prayer_on_img = cv.imread('../screenshots/control_panel_bars/prayer_on.png', cv.IMREAD_UNCHANGED)

prayer_off_bar = prayer_off_img[Regions.CP_PRAYER_BAR.as_slice()]
prayer_on_bar = prayer_on_img[Regions.CP_PRAYER_BAR.as_slice()]

x, y = prayer_off_bar.shape[1] // 2, prayer_off_bar.shape[0] - 10
prayer_off_color = prayer_off_bar[y][x]
prayer_on_color = prayer_on_bar[y][x]

print("Prayer Off Color:", prayer_off_color)
print("Prayer On Color:", prayer_on_color)
print()


def color_distance(color1, color2):
    return cv.norm(color1.astype(np.int32) - color2.astype(np.int32))


x, y = Regions.CP_PRAYER_BAR.w // 2, Regions.CP_PRAYER_BAR.h - 5
subimage = haystack_img[Regions.CP_PRAYER_BAR.as_slice()]
pixel = subimage[y][x]

prayer_off_score = color_distance(pixel, prayer_off_color)
prayer_on_score = color_distance(pixel, prayer_on_color)
min_score = min(prayer_off_score, prayer_on_score)
state = "Prayer Off" if (min_score == prayer_off_score) else "Prayer On"
print(state, '-', min_score)

cv.imshow("Prayer Off Bar", prayer_off_bar)
cv.imshow("Prayer On Bar", prayer_on_bar)
cv.waitKey()
