"""
Detect 'accept' -> click 'accept'
detect from my inventory the thing I am selling, click on it
detect from their inventory what I am buying, make sure it's selected
click trade
"""

import cv2, numpy as np, time
import pyautogui as pya
from PIL import ImageGrab

class Trader:
    def __init__(self):
        self.thresh = 0.9

    def source_preprocess(self, check_for: str):
        check = ImageGrab.grab()
        check.save(f'source_imgs/{check_for}.png')
        check_for_to_arr = cv2.imread(f'source_imgs/{check_for}.png')
        screenshot_processed = cv2.cvtColor(check_for_to_arr, cv2.COLOR_BGR2RGB)
        return screenshot_processed
    
    def template_preprocess(self, check_against: str):
        check_against = cv2.imread(f'template_imgs/{check_against}.png')
        check_against_preprocessed= cv2.cvtColor(check_against, cv2.COLOR_BGR2RGB)
        return check_against_preprocessed

    def move_and_click(self, check_for: str, check_against: str):
        re_use = self.if_on_screen(check_for, check_against)
        if re_use[0] > self.thresh: # checks if above threshold to click
            pya.moveTo( re_use[1][0], re_use[1][1] )
            print(f'moving to -> { re_use[1][0], re_use[1][1] / 2 }\nclicking..')
            pya.click()

    def get_match_coords(self, check_for: str, check_against: str):
        source = self.source_preprocess(check_for)
        template = self.template_preprocess(check_against)

        res = cv2.matchTemplate(source, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(res >= self.thresh)
        matches = list(zip(locations[1], locations[0]))
        print(matches)

    def if_on_screen(self, check_for: str, check_against: str):
        source = self.source_preprocess(check_for)
        template = self.template_preprocess(check_against)
        result = cv2.matchTemplate(source, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val: print(f'{check_for} processed successfully..\nconfidence -> {max_val}')
        return [ max_val , (int(max_loc[0]) / 2 , int(max_loc[1]) / 2) ]
    
    def delay(self, seconds: int):
        print(f'waiting for {seconds} seconds..')
        return time.sleep(seconds)
    
trader = Trader()

while True:
    trader.get_match_coords('match_test', 'glife_macos')
    """
    try: 
        trader.get_match_coords('match_test', 'glife_macos')
    except: print('not found')
    trader.delay(1)
    """


    

