import pyautogui
import cv2
import numpy as np

while True:
    screen = pyautogui.screenshot()
    screen_arr = np.array(screen)
    screen_arr = cv2.cvtColor(screen_arr, cv2.COLOR_RGB2BGR)
    cv2.imshow("game capture", screen_arr)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cv2.destroyAllWindows()