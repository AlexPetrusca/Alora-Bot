import cv2 as cv
import numpy as np
from pytesseract import pytesseract

from src.vision import vision
from src.vision.regions import Regions

haystack_img = cv.imread('../screenshots/damage_ui/present_68.png', cv.IMREAD_UNCHANGED)
# haystack_img = cv.imread('../screenshots/alt_macbook/cerb_fight_2.png', cv.IMREAD_UNCHANGED)
damage_ui_image = np.ndarray.copy(haystack_img[Regions.COMBAT_INFO.as_slice()])

ocr1 = pytesseract.image_to_string(damage_ui_image, config='--psm 6').strip()
print(" - basic ocr:", ocr1)

grayscale = cv.cvtColor(damage_ui_image, cv.COLOR_BGR2GRAY)
threshold = cv.threshold(grayscale, 120, 255, cv.THRESH_BINARY)[1]
blur = cv.blur(threshold, (3, 3))
morph = cv.morphologyEx(blur, cv.MORPH_CLOSE, np.ones((2, 2), np.uint8))
ocr2 = pytesseract.image_to_string(morph, config='--psm 6').strip()
print(" - advanced ocr:", ocr2)

print(vision.read_text(damage_ui_image))
print(vision.read_text(damage_ui_image, config='--psm 6'))

cv.imshow('Screenshot', haystack_img)
cv.imshow('Damage UI', damage_ui_image)
cv.imshow('Grayscale', grayscale)
cv.imshow('Threshold', threshold)
cv.imshow('Blur', blur)
cv.imshow('Morph', morph)
cv.waitKey()
cv.destroyAllWindows()
