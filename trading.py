"""
Detect 'accept' -> click 'accept'
detect from my inventory the thing I am selling, click on it
detect from their inventory what I am buying, make sure it's selected
click trade
"""

import cv2
import pyautogui as pya
from PIL import ImageGrab

class Trader:
    def __init__(self):
        pass

    def move_and_click(self, check_for: str, check_against: str):
        re_use = self.if_on_screen(check_for, check_against)
        if re_use[0] > self.thresh: 
            pya.moveTo( re_use[1][0], re_use[1][1] )
            print(f'moving to -> { re_use[1][0], re_use[1][1] / 2 }\nclicking..')
            pya.click()

    def if_on_screen(self, check_for: str, check_against: str):
        check = ImageGrab.grab()
        check.save(f'{check_for}.png')
        check_for_to_arr = cv2.imread(f'{check_for}.png')
        preprocess_check_for = cv2.cvtColor(check_for_to_arr, cv2.COLOR_BGR2RGB)

        check_against = cv2.imread(f'pics_to_check_for/{check_against}.png')
        preprocess_check_against= cv2.cvtColor(check_against, cv2.COLOR_BGR2RGB)

        result = cv2.matchTemplate(preprocess_check_for, preprocess_check_against, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val: print(f'{check_for} processed successfully..\nconfidence -> {max_val}')
        return [ max_val , (int(max_loc[0]) / 2 , int(max_loc[1]) / 2) ]
    
trader = Trader()

while True:
    if trader.if_on_screen():
        trader.move_and_click()


    

