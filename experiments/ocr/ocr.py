import cv2 as cv
import numpy as np
import pytesseract

img = cv.imread('../screenshots/full_inventory.png', cv.IMREAD_UNCHANGED)

hover_action_image = np.ndarray.copy(img[74:114, 0:800])
print(pytesseract.image_to_string(hover_action_image).strip())

chat_line_image = np.ndarray.copy(img[2106:2144, 14:994])
print(pytesseract.image_to_string(chat_line_image).strip())

cv.imshow("Hover Action", hover_action_image)
cv.imshow("Chat Line", chat_line_image)
cv.waitKey(0)
