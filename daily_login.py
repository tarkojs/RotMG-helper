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


    def select_window(self, app_name: str, launch_command: str = None):
        """
        Finds and activates the specified window with the given `app_name`.
    
        If the window is not found, it will attempt to launch it using the optional `launch_command`
        parameter (if provided).
        
        Parameters:
        -----------
        app_name: str
            The name of the window to find and activate.
            
        launch_command: str, optional
            A command-line command to launch the application if it is not found.
            This parameter is required for macOS and optional for Windows.
        """
        try:
            if sys.platform.startswith('darwin'):
                script = f'tell application "{app_name}" to activate'
                subprocess.call(['osascript', '-e', script])
                rotmg_window = app_name
                self.delay(5, 'assuring the app is launched')
            if sys.platform.startswith('win'):
                rotmg_window = win32gui.FindWindow(None, app_name)
                win32gui.SetForegroundWindow(rotmg_window)
            elif rotmg_window == 0 and launch_command is not None:
                subprocess.Popen(launch_command, shell = True)
                self.delay(5, 'assuring the app is launched')
                rotmg_window = win32gui.FindWindow(None, app_name)
                win32gui.SetForegroundWindow(rotmg_window)
            print(f'successfully found the RotMG window and set it as active.')
        except Exception as e: print(f'failed to select the RotMG window and set it as active: {str(e)}')
        

    def if_on_screen(self, source: str, template: str):
        """
        Check if the given template is present on the screen in the given source.
        :param source: Name of the screen source.
        :param template: Name of the template to look for.
        :return: Confidence of the template match and location of the template on the screen.
        """
        check = ImageGrab.grab()
        check.save(f'source_imgs/{source}.png')
        source_to_arr = cv2.imread(f'source_imgs/{source}.png')
        preprocess_source = cv2.cvtColor(source_to_arr, cv2.COLOR_BGR2RGB)

        template = cv2.imread(f'template_imgs/{template}.png')
        preprocess_template= cv2.cvtColor(template, cv2.COLOR_BGR2RGB)

        result = cv2.matchTemplate(preprocess_source, preprocess_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val: print(f'{source} processed successfully..\nconfidence -> {max_val}')
        return [ max_val , (int(max_loc[0]) / 2 , int(max_loc[1]) / 2) ]

    
    def move_and_click(self, source: str, template: str):
        """
        Moves the mouse to the location of the template on the screen and clicks it if the confidence value is above the threshold.
        :param source: Name of the screen source.
        :param template: Name of the template to look for.
        """
        re_use = self.if_on_screen(source, template)
        if re_use[0] > self.thresh: 
            pya.moveTo( re_use[1][0], re_use[1][1] )
            print(f'moving to -> { re_use[1][0], re_use[1][1] / 2 }\nclicking..')
            pya.click()

    
    def delay(self, seconds: int, reason: str):
        print(f'waiting for {seconds} seconds -> {reason}')
        return time.sleep(seconds)


login = Daily_Login()
login.select_window('RotMG Exalt Launcher', 'RotMG Exalt Launcher')
login.move_and_click('play_button_live', 'play_button')
while True:
    print(f'looking for "Go & Claim" prompt.')
    login.delay(5, 'waiting for the prompt')
    if login.if_on_screen('go_and_claim_live', 'go_and_claim')[0]:
        print(f'Go & Claim prompt found..')
        login.move_and_click('go_and_claim_live', 'go_and_claim')
        break
