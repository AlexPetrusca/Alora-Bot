import cv2 as cv
import numpy as np

from src.vision.regions import Regions

haystack_img = cv.imread('../screenshots/control_panel_bars/no_prayer.png', cv.IMREAD_UNCHANGED)
healthy_img = cv.imread('../screenshots/control_panel_bars/no_prayer.png', cv.IMREAD_UNCHANGED)
poison_img = cv.imread('../screenshots/control_panel_bars/poison.png', cv.IMREAD_UNCHANGED)
venom_img = cv.imread('../screenshots/control_panel_bars/venom.png', cv.IMREAD_UNCHANGED)

healthy_bar = healthy_img[Regions.CP_HITPOINTS_BAR.as_slice()]
poison_bar = poison_img[Regions.CP_HITPOINTS_BAR.as_slice()]
venom_bar = venom_img[Regions.CP_HITPOINTS_BAR.as_slice()]

x, y = healthy_bar.shape[1] // 2, healthy_bar.shape[0] - 10
healthy_color = healthy_bar[y][x]
poison_color = poison_bar[y][x]
venom_color = venom_bar[y][x]

print("Healthy Color:", healthy_color)
print("Poison Color:", poison_color)
print("Venom Color:", venom_color)
print()


def color_distance(color1, color2):
    return cv.norm(color1.astype(np.int32) - color2.astype(np.int32))


print("Healthy vs Poison:", color_distance(poison_color, healthy_color))
print("Healthy vs Venom:", color_distance(venom_color, healthy_color))
print("Poison vs Venom:", color_distance(venom_color, poison_color))
print("Similar Colors:", color_distance(venom_bar[y - 20][x - 2], venom_color))
print()

x, y = Regions.CP_HITPOINTS_BAR.w // 2, Regions.CP_HITPOINTS_BAR.h - 5
subimage = haystack_img[Regions.CP_HITPOINTS_BAR.as_slice()]
pixel = subimage[y][x]

state = "Healthy"
score = color_distance(pixel, healthy_color)
if color_distance(pixel, poison_color) < score:
    state = "Poison"
    score = color_distance(pixel, poison_color)
if color_distance(pixel, venom_color) < score:
    state = "Venom"
    score = color_distance(pixel, venom_color)

print(state, '-', score)

cv.imshow("Healthy Bar", healthy_bar)
cv.imshow("Poison Bar", poison_bar)
cv.imshow("Venom Bar", venom_bar)
cv.waitKey()
