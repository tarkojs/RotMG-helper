import pyautogui as pya
import cv2
from PIL import ImageGrab

"""
Logs in automatically using the launcher and acquires the daily login item
"""

class Daily_Login():

    def __init__(self):
        self.thresh = 0.8


    def if_on_screen(self, check_for: str, check_against: str):
        check = ImageGrab.grab(check_for)
        check.save(f'{check_for}.png')
        check_for_to_arr = cv2.imread(f'{check_for}.png')
        preprocess_check_for = cv2.cvtColor(check_for_to_arr, cv2.COLOR_BGR2RGB)

        check_against = cv2.imread(f'pics_to_check_for/{check_against}.png')
        preprocess_check_against= cv2.cvtColor(check_against, cv2.COLOR_BGR2RGB)

        result = cv2.matchTemplate(preprocess_check_for, preprocess_check_against, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        return [ max_val , (int(max_loc[0] / 2) , int(max_loc[1] / 2)) ]

    
    def move_and_click(self, check_for: str, check_against: str):
        re_use = self.if_on_screen(check_for, check_against)
        if re_use[0] > 0.8: 
            pya.moveTo( loc_x = re_use[1][0], loc_y = re_use[1][1] )
            print(f'moving to -> { re_use[1][0], re_use[1][1] / 2 }')


login = Daily_Login()
login.move_and_click('play_button_live', 'play_button')
