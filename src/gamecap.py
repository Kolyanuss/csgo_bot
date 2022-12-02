import cv2
import numpy as np
import time
import mss

i = 0

with mss.mss() as sct:
    monitor = {"top": 26, "left": 0, "width": 800, "height": 600}

    i = 0
    start_time = time.time()
    while True:
        img = np.array(sct.grab(monitor))
        cv2.imshow("OpenCV", img)
        i += 1
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

    mytime = time.time() - start_time
    print("avg fps is: ", 1/(mytime/i))
