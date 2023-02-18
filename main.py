from PIL import ImageGrab
import pyautogui as pya
import numpy as np
import pytesseract
import cv2

"""
Currently has two versions of auto nexus
Both work -> consistency depends on speed of computer
"""

def analyze_image_color(hp_coords_x, hp_coords_y):
    """
    Analyzes and returns the color of the HP bar
    """
    screenshot = np.array(ImageGrab.grab())
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    color = gray[hp_coords_y, hp_coords_x]
    return int(color)


def detect_nexus():
    """
    If the color is too dark -> nexus
    """
    check_color = analyze_image_color()
    if check_color != 0 and check_color < 68: pya.press('r')
    print(f'detected low hp (color number -> {check_color}) -> nexusing..')


def get_image( left_x, top_y, right_x, bottom_y ):
    string, nums, too_low = '', '0123456789', ['1', '2']
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
            hp = int(string)
            corr_string = string

        if (hp < 250 and len(str(hp)) == 3) or corr_string[0] in too_low:
            print(f'nexusing. hp -> {hp}, hp length -> {len(str(hp))}\n, corr_string -> {corr_string[0]}')
            pya.keyDown('r')
            pya.keyUp('r')
    except Exception: print(f'failed to nexus.')



def necromancer_heal():
    print('using ability.')
    pya.press('space')


def main():
    while True:
        analyze_image_color()
        detect_nexus()


if __name__ == '__main__':
    main()