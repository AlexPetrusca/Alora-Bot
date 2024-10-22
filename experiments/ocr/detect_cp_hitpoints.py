import cv2 as cv
import numpy as np
from pytesseract import pytesseract

from src.vision import vision
from src.vision.color import Color
from src.vision.regions import Regions

haystack_img = cv.imread('../screenshots/control_panel_bars/no_prayer.png', cv.IMREAD_UNCHANGED)
cp_hp_image = np.ndarray.copy(haystack_img[Regions.CP_PRAYER.as_slice()])

ocr1 = pytesseract.image_to_string(cp_hp_image, config='--psm 6').strip()
print(" - basic ocr:", ocr1)

hsv_damage_ui_image = cv.cvtColor(cp_hp_image, cv.COLOR_BGR2HSV)
lower_limit, upper_limit = Color.WHITE.get_limits(0.1, 0.5, 0.5)
mask = cv.inRange(hsv_damage_ui_image, lower_limit, upper_limit)
ocr2 = pytesseract.image_to_string(mask, config='--psm 6').strip()
print(" - advanced ocr:", ocr2)

print(vision.read_text(cp_hp_image))
print(vision.read_text(cp_hp_image, config='--psm 6'))

cv.imshow('Screenshot', haystack_img)
cv.imshow('Hitpoints', cp_hp_image)
cv.imshow('Hitpoints Mask', mask)
cv.waitKey()
cv.destroyAllWindows()
