import pyautogui as pya
import pytesseract
import cv2
from PIL import ImageGrab
from time import sleep
import numpy as np
#myconfig = r'--psm 3 --oem 3'

def analyze_img():
    x, y = 1254*2, 337*2
    screenshot = np.array(ImageGrab.grab())
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    color = gray[y, x]
    print(color)
    return int(color)


def detect_nexus():
    if analyze_img() < 67:
        pya.press('r')



def get_image(left_x, top_y, right_x, bottom_y):
    string = ''
    nums = '012345679'
    too_low = ['1', '2']
    heal_hp = ['3', '4']
    live_img = np.asarray(ImageGrab.grab( bbox = (left_x*2, top_y*2, right_x*2, bottom_y*2) ))
    text = pytesseract.image_to_string(live_img)
    try:
        for symbol in text[:3]:
            if symbol == 'S': string += '2'
            if symbol == 's': string += '5'
            if symbol == 'o': string += '0'
            if symbol == 'O': string += '0'
            if symbol in nums: string += str(symbol)
            
        print(f'string -> {string}, length -> {len(string)}')

        if len(string) == 3:
            print('success')
            hp = int(string)
            corr_string = string
            if corr_string[0] in heal_hp:
                necromancer_heal()

        if (hp < 250 and len(str(hp)) == 3) or corr_string[0] in too_low:
            print(f'nexusing. hp -> {hp}, hp length -> {len(str(hp))}\n, corr_string -> {corr_string[0]}')
            pya.keyDown('r')
            pya.keyUp('r')
    except:
        #print('failed')
        pass


def necromancer_heal():
    print('using ability.')
    pya.press('space')


def main():
    while True:
        analyze_img()
        detect_nexus()
        #get_image(1276, 316, 1387, 371)


if __name__ == '__main__':
    main()