import cv2 as cv
import numpy as np

from src.vision.regions import Regions

haystack_img = cv.imread('screenshots/control_panel_bars/no_prayer.png', cv.IMREAD_UNCHANGED)
# haystack_img = cv.imread('../resources/resources/screenshots/alt_macbook/edgeville.png', cv.IMREAD_UNCHANGED)

minimap_image = np.ndarray.copy(haystack_img[Regions.MINIMAP.as_slice()])
inventory_image = np.ndarray.copy(haystack_img[Regions.INVENTORY.as_slice()])
hover_action_image = np.ndarray.copy(haystack_img[Regions.HOVER_ACTION.as_slice()])
bank_image = np.ndarray.copy(haystack_img[Regions.BANK.as_slice()])
chat_image = np.ndarray.copy(haystack_img[Regions.CHAT.as_slice()])
latest_chat_image = np.ndarray.copy(haystack_img[Regions.LATEST_CHAT.as_slice()])
cp_hitpoints_bar_image = np.ndarray.copy(haystack_img[Regions.CP_HITPOINTS_BAR.as_slice()])
cp_prayer_bar_image = np.ndarray.copy(haystack_img[Regions.CP_PRAYER_BAR.as_slice()])
cp_hitpoints_image = np.ndarray.copy(haystack_img[Regions.CP_HITPOINTS.as_slice()])
cp_prayer_image = np.ndarray.copy(haystack_img[Regions.CP_PRAYER.as_slice()])

cv.imshow('Screenshot', haystack_img)
cv.imshow('Minimap', minimap_image)
cv.imshow('Inventory', inventory_image)
cv.imshow('Hover Action', hover_action_image)
cv.imshow('Bank', bank_image)
cv.imshow('Chat', chat_image)
cv.imshow('Latest Chat Message ', latest_chat_image)
cv.imshow('Control Panel Hitpoints Bar', cp_hitpoints_bar_image)
cv.imshow('Control Panel Prayer Bar', cp_prayer_bar_image)
cv.imshow('Control Panel Hitpoints', cp_hitpoints_image)
cv.imshow('Control Panel Prayer', cp_prayer_image)
cv.waitKey()
cv.destroyAllWindows()
