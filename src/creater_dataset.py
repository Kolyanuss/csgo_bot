import pyautogui
import cv2
import numpy as np
import time
from pynput import keyboard

path_to_save = "temp_img"


def foo():
    screen = pyautogui.screenshot()
    screen_arr = np.array(screen)
    screen_arr = screen_arr[27:890, 768:, :]
    screen_arr = cv2.cvtColor(screen_arr, cv2.COLOR_RGB2BGR)
    cv2.imwrite(path_to_save+"/screen_" + str(time.time()) + ".png", screen_arr)    


def checker(key):
    # print(f'{key} released')
    if key == keyboard.Key.alt_l:
        foo()
    if key == keyboard.Key.esc:
        return False


with keyboard.Listener(on_press=checker) as listener:
    listener.join()
