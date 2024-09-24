import cv2 as cv
import numpy as np
import pytesseract

from src.util.common import hide_ui, get_color_limits
from src.vision import vision
from src.vision.color import Color

screenshot_image = cv.imread('../resources/experiments/screenshot/edgeville.png', cv.IMREAD_UNCHANGED)
chat_line_image = np.ndarray.copy(screenshot_image[2106:2144, 14:994])

_, threshold = cv.threshold(hide_ui(screenshot_image), 0, 255, cv.THRESH_BINARY)
hsv_threshold = cv.cvtColor(threshold, cv.COLOR_BGR2HSV)
cv.imshow("Threshold", threshold)

yellow_lower_limit, upper_limit = get_color_limits(Color.YELLOW.value)
yellow_mask = cv.inRange(hsv_threshold, yellow_lower_limit, upper_limit)
cv.imshow("Yellow Mask", yellow_mask)

red_lower_limit, upper_limit = get_color_limits(Color.RED.value)
red_mask = cv.inRange(hsv_threshold, red_lower_limit, upper_limit)
cv.imshow("Red Mask", red_mask)

screenshot_threshold = cv.cvtColor(screenshot_image, cv.COLOR_BGR2HSV)
white_mask = cv.inRange(screenshot_threshold, np.array([0, 0, 255]), np.array([255, 100, 255]))
cv.imshow("White Mask", white_mask)

tile_xy = vision.locate_contour(screenshot_image, Color.YELLOW.value)
if tile_xy is not None:
    tile_x, tile_y = (round(tile_xy[0]), round(tile_xy[1]))
    cv.rectangle(screenshot_image, (tile_x - 5, tile_y - 5), (tile_x + 5, tile_y + 5), (0, 255, 0), -1)

cerb_xy = vision.locate_contour(screenshot_image, Color.RED.value)
if cerb_xy is not None:
    cerb_x, cerb_y = (round(cerb_xy[0]), round(cerb_xy[1]))
    cv.rectangle(screenshot_image, (cerb_x - 5, cerb_y - 5), (cerb_x + 5, cerb_y + 5), (0, 255, 0), -1)

chat_line = pytesseract.image_to_string(chat_line_image).strip()
cv.putText(screenshot_image, chat_line, (10, 50), cv.FONT_HERSHEY_SIMPLEX,
           1, (0, 0, 255), 2, cv.LINE_AA)

cv.imshow("Screenshot", screenshot_image)
cv.waitKey(0)
