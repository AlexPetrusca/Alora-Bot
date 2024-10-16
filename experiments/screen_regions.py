import cv2 as cv
import numpy as np

from src.vision.regions import Regions

haystack_img = cv.imread('screenshots/full_switch.png', cv.IMREAD_UNCHANGED)
# haystack_img = cv.imread('../resources/resources/screenshots/alt_macbook/edgeville.png', cv.IMREAD_UNCHANGED)
minimap_image = np.ndarray.copy(haystack_img[Regions.MINIMAP.as_slice()])
inventory_image = np.ndarray.copy(haystack_img[Regions.INVENTORY.as_slice()])
hover_action_image = np.ndarray.copy(haystack_img[Regions.HOVER_ACTION.as_slice()])
bank_image = np.ndarray.copy(haystack_img[Regions.BANK.as_slice()])
chat_image = np.ndarray.copy(haystack_img[Regions.CHAT.as_slice()])
latest_chat_image = np.ndarray.copy(haystack_img[Regions.LATEST_CHAT.as_slice()])

cv.imshow('Screenshot', haystack_img)
cv.imshow('Minimap', minimap_image)
cv.imshow('Inventory', inventory_image)
cv.imshow('Hover Action', hover_action_image)
cv.imshow('Bank', bank_image)
cv.imshow('Chat', chat_image)
cv.imshow('Latest Chat Message', latest_chat_image)
cv.waitKey()
cv.destroyAllWindows()
