import pyautogui
import cv2
import numpy as np
import time

path_to_save = "temp_img"

while True:
    screen = pyautogui.screenshot()
    screen_arr = np.array(screen)
    screen_arr = screen_arr[:1024, 960:, :]
    screen_arr = cv2.cvtColor(screen_arr, cv2.COLOR_RGB2BGR)
    # cv2.imshow("game capture", [screen_arr])

    if cv2.waitKey(1) & 0xFF == ord('c'):
        cv2.imwrite(path_to_save+"/screen_" + str(time.time()) + ".png", screen_arr)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()