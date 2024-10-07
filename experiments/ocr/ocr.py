import cv2 as cv
import numpy as np
import pytesseract

from src.vision import vision
from src.vision.regions import Regions

img = cv.imread('../screenshots/breadcrumb_labels.png', cv.IMREAD_UNCHANGED)

hover_action_image = np.ndarray.copy(img[Regions.HOVER_ACTION.as_slice()])
print(pytesseract.image_to_string(hover_action_image).strip())
print(vision.read_text(hover_action_image))
print()

chat_line_image = np.ndarray.copy(img[Regions.LATEST_CHAT.as_slice()])
print(pytesseract.image_to_string(chat_line_image).strip())
print(vision.read_text(chat_line_image))

cv.imshow("Hover Action", hover_action_image)
cv.imshow("Chat Line", chat_line_image)
cv.waitKey(0)
