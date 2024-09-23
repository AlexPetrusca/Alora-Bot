import cv2 as cv
import numpy as np
import pytesseract

img = cv.imread('../resources/experiments/screenshot/cerberus/1.png', cv.IMREAD_UNCHANGED)
chat_line_image = np.ndarray.copy(img[2106:2144, 14:994])

print(pytesseract.image_to_string(chat_line_image))

cv.imshow("OCR", chat_line_image)
cv.waitKey(0)
# 7 1053
# 497 1072