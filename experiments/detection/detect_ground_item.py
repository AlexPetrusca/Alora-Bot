import cv2 as cv
from src.vision import vision
from src.vision.color import Color
from src.vision.vision import mask_ui

# COLOR = Color.DEFAULT_VALUE  # 0, 200
# COLOR = Color.HIGHLIGHTED_VALUE
COLOR = Color.LOW_VALUE
# COLOR = Color.MEDIUM_VALUE
# COLOR = Color.HIGH_VALUE  # 200, 200
# COLOR = Color.INSANE_VALUE

screenshot_image = mask_ui(cv.imread('../screenshots/ground_items/ground_items.png', cv.IMREAD_UNCHANGED))
screenshot_threshold = cv.cvtColor(screenshot_image, cv.COLOR_BGR2HSV)
lower_limit, upper_limit = COLOR.get_limits()
mask = cv.inRange(screenshot_threshold, lower_limit, upper_limit)

loc = vision.locate_ground_item(screenshot_image)
if loc is not None:
    x, y = loc
    cv.rectangle(screenshot_image, (x - 5, y - 5), (x + 5, y + 5), color=(0, 0, 255), thickness=-1, lineType=cv.LINE_AA)

contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
for contour in contours:
    if cv.contourArea(contour) > 250:
        x, y, w, h = cv.boundingRect(contour)
        cv.rectangle(screenshot_image, (x, y), (x + w, y + h), color=(0, 0, 255), thickness=2, lineType=cv.LINE_AA)

cv.imshow("Mask", mask)
cv.imshow("Screenshot", screenshot_image)
cv.waitKey(0)
