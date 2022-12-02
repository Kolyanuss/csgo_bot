import cv2
import numpy as np
import time
import mss

i = 0

with mss.mss() as sct:
    monitor = {"top": 0, "left": 0, "width": 600, "height": 500}

    i = 0
    start_time = time.time()
    while i<500:
        img = np.array(sct.grab(monitor))
        cv2.imshow("OpenCV/Numpy normal", img)
        i += 1
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

    mytime = time.time() - start_time
    print("avg fps is: ", 1/(mytime/i))
