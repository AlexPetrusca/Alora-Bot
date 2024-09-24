import cv2 as cv
import numpy as np
from pytesseract import pytesseract

from src.vision import vision

haystack = cv.imread('../resources/experiments/screenshot/damage_ui/not_present.png', cv.IMREAD_UNCHANGED)

health_img = haystack[188:212, 2978:3018]  # w = 40, h = 24
prayer_img = haystack[256:280, 2978:3018]  # w = 40, h = 24
energy_img = haystack[320:344, 2996:3036]  # w = 40, h = 24
spec_img = haystack[372:396, 3044:3084]  # w = 40, h = 24

grayscale = cv.cvtColor(prayer_img, cv.COLOR_BGR2GRAY)
threshold = cv.threshold(grayscale, 128, 255, cv.THRESH_BINARY)[1]
dilation = cv.dilate(threshold, np.ones((1, 2), np.uint8), iterations=1)
number = pytesseract.image_to_string(dilation, config='--psm 6').strip()
print("Experiment:", number)
print()

print("Health Text:", vision.read_text(health_img, config='--psm 6'))
print("Prayer Text:", vision.read_text(prayer_img, config='--psm 6'))
print("Energy Text:", vision.read_text(energy_img, config='--psm 6'))
print("Special Text:", vision.read_text(spec_img, config='--psm 6'))
print()

print("Health:", vision.read_int(health_img))
print("Prayer:", vision.read_int(prayer_img))
print("Energy:", vision.read_int(energy_img))
print("Special:", vision.read_int(spec_img))

cv.imshow("Grayscale", grayscale)
cv.imshow("Threshold", threshold)
cv.imshow("Dilation", dilation)
cv.waitKey(0)
