import cv2 as cv

from src.vision.vision import mask_ui

haystack_img = cv.imread('screenshots/slayer/nechryael.png', cv.IMREAD_UNCHANGED)

mask_ui(haystack_img)

cv.imshow('Screenshot', haystack_img)
cv.waitKey()
cv.destroyAllWindows()
