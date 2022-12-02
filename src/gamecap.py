import cv2
import numpy as np
import time
import mss

sum_time = 0
i = 0

with mss.mss() as sct:
    # The screen part to capture
    monitor = {"top": 0, "left": 0, "width": 600, "height": 500}

    i = 0
    while "Screen capturing":
        last_time = time.time()

        img = np.array(sct.grab(monitor))
        cv2.imshow("OpenCV/Numpy normal", img)

        mytime = time.time() - last_time
        print(f"fps: {1 / mytime}")
        i += 1
        sum_time += mytime

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

    print("avg fps is: ", 1/(sum_time/i))
