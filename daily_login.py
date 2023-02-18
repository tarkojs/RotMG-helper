import pyautogui as pya
import cv2
import sys
import time
from PIL import ImageGrab

"""
Logs in automatically using the launcher
Acquires the daily login item
"""

if sys.platform.startswith('darwin'): import subprocess
elif sys.platform.startswith('win'): import win32gui
else: raise NotImplementedError('your OS has not been implemented')


class Daily_Login():

    def __init__(self):
        self.thresh = 0.8


    def select_window(self, app_name: str):
        try:
            if sys.platform.startswith('darwin'):
                script = f'tell application "{app_name}" to activate'
                subprocess.call(['osascript', '-e', script])
            if sys.platform.startswith('win'):
                rotmg_window = win32gui.FindWindow(None, app_name)
                win32gui.SetForegroundWindow(rotmg_window)
            print(f'successfully found the RotMG window and set it as active.')
        except Exception as e: print(f'failed to select the RotMG window and set it as active: {str(e)}')
        

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

    
    def move_and_click(self, check_for: str, check_against: str):
        re_use = self.if_on_screen(check_for, check_against)
        if re_use[0] > self.thresh: 
            pya.moveTo( re_use[1][0], re_use[1][1] )
            print(f'moving to -> { re_use[1][0], re_use[1][1] / 2 }\nclicking..')
            pya.click()

    
    def delay(self, seconds: int):
        print(f'waiting for {seconds} seconds..')
        return time.sleep(seconds)


login = Daily_Login()
login.select_window('RotMG Exalt Launcher')
login.move_and_click('play_button_live', 'play_button')
while True:
    print(f'looking for "Go & Claim" prompt.')
    login.delay(5)
    if login.if_on_screen('go_and_claim_live', 'go_and_claim')[0]:
        print(f'"Go & Claim prompt found..')
        login.move_and_click('go_and_claim_live', 'go_and_claim')
        break
