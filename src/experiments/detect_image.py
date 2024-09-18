import cv2 as cv
import numpy as np

haystack_img = cv.imread('../../resources/screenshot/slayer/nechryael.png', cv.IMREAD_UNCHANGED)
minimap_image = np.ndarray.copy(haystack_img[74:420, 2952:3394])
inventory_image = np.ndarray.copy(haystack_img[1568:2234, 2910:3392])
hover_action_image = np.ndarray.copy(haystack_img[74:114, 0:800])
needle_img = cv.imread('../../resources/target/compass.png', cv.IMREAD_UNCHANGED)

# hide_ui(haystack_img)

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

cv.rectangle(haystack_img, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

cv.imshow('Screenshot', haystack_img)
cv.imshow('Minimap', minimap_image)
cv.imshow('Inventory', inventory_image)
cv.imshow('Hover Action', hover_action_image)
cv.waitKey()
cv.destroyAllWindows()
