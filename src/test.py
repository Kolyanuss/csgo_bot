import cv2
import numpy as np
import time
import mss
import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
monitor = {"top": 26, "left": 0, "width": 640, "height": 640}
sct = mss.mss()
i = 0
start_time = time.time()

while True:
    frame = np.array(sct.grab(monitor))
    # ----------

    results = model(frame, size=640)  # includes NMS
    results.print()
    
    # results

    # ----------
    cv2.imshow("OpenCV", np.array(results))
    i += 1
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
mytime = time.time() - start_time
print("avg fps is: ", 1/(mytime/i))
