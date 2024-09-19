import cv2 as cv
import numpy as np
import pytesseract

img = cv.imread('../../resources/experiments/screenshot/dev/location_camera.png', cv.IMREAD_UNCHANGED)
hover_action_image = np.ndarray.copy(img[74:114, 0:800])

print(pytesseract.image_to_string(hover_action_image))
