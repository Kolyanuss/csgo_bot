import cv2
import numpy as np
import time
import mss

sct = mss.mss()
monitor = {"top": 26, "left": 0, "width": 800, "height": 600}
i = 0
start_time = time.time()

while True:
    frame = np.array(sct.grab(monitor))
    # ----------

    # add: YOLO

    # ----------
    cv2.imshow("OpenCV", frame)
    i += 1
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
# vs.stop()
mytime = time.time() - start_time
print("avg fps is: ", 1/(mytime/i))
