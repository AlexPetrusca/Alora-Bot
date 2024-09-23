import cv2 as cv
import numpy as np
from pytesseract import pytesseract

haystack_img = cv.imread('../resources/experiments/screenshot/damage_ui/present_68.png', cv.IMREAD_UNCHANGED)
needle_img = cv.imread('../resources/experiments/target/damage_ui.png', cv.IMREAD_UNCHANGED)

result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

# if max_val < THRESHOLD_LOW:
#     print('not found', '-', max_val)
#     exit(1)

print('found', '-', max_val)

needle_w = needle_img.shape[1]
needle_h = needle_img.shape[0]

top_left = max_loc
bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

damage_ui_image = np.ndarray.copy(haystack_img[152:192, 12:264])
print(f'OCR: "{pytesseract.image_to_string(damage_ui_image).strip()}"')

cv.rectangle(haystack_img, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

cv.imshow('Screenshot', haystack_img)
cv.imshow('Damage UI', damage_ui_image)
cv.waitKey()
cv.destroyAllWindows()
