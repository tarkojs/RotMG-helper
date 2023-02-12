import pyautogui as pya
import cv2
import numpy as np
from PIL import ImageGrab


inv_coords = (1232*2, 455*2, 1433*2, 555*2)
while True:
    #located = pya.locateCenterOnScreen('potion_hp.png')
    #print(located)

    img = ImageGrab.grab()
    img.save('potion.png')

    if_blind_to_array = cv2.imread('potion.png')
    if_blind = cv2.cvtColor(if_blind_to_array, cv2.COLOR_BGR2RGB)

    blind_to_array = cv2.imread('potion_hp.png')
    blind_img = cv2.cvtColor(blind_to_array, cv2.COLOR_BGR2RGB)

    res = cv2.matchTemplate(if_blind, blind_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    print(min_val, max_val, min_loc, max_loc)