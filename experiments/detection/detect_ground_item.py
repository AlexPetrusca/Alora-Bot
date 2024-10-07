import cv2 as cv
from src.vision.color import Color, get_color_limits
from src.vision.vision import mask_ui

# COLOR = Color.DEFAULT_VALUE.value  # 0, 200
# COLOR = Color.HIGHLIGHTED_VALUE.value
# COLOR = Color.LOW_VALUE.value
# COLOR = Color.MEDIUM_VALUE.value
COLOR = Color.HIGH_VALUE.value  # 200, 200
# COLOR = Color.INSANE_VALUE.value

screenshot_image = mask_ui(cv.imread('../screenshots/ground_items/ground_items.png', cv.IMREAD_UNCHANGED))
screenshot_threshold = cv.cvtColor(screenshot_image, cv.COLOR_BGR2HSV)
lower_limit, upper_limit = get_color_limits(COLOR)
mask = cv.inRange(screenshot_threshold, lower_limit, upper_limit)

contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
for contour in contours:
    if cv.contourArea(contour) > 500:
        x, y, w, h = cv.boundingRect(contour)
        cv.rectangle(screenshot_image, (x, y), (x + w, y + h), color=(0, 0, 255), thickness=2, lineType=cv.LINE_AA)

cv.imshow("Mask", mask)
cv.imshow("Screenshot", screenshot_image)
cv.waitKey(0)
