import pyautogui
import cv2
import numpy as np
import time

while True:
    begin_time = time.time()

    screen = pyautogui.screenshot()
    screen_arr = np.array(screen)
    screen_arr = screen_arr[27:890, 768:, :]
    screen_arr = cv2.cvtColor(screen_arr, cv2.COLOR_RGB2BGR)
    cv2.imshow("game capture", screen_arr)

    print(time.time()-begin_time)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cv2.destroyAllWindows()