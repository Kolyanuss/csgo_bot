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

    # add: use YOLO

    # draw a box around the models and the class name
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # rescale the face coordinates
        top = int(top * r)
        right = int(right * r)
        bottom = int(bottom * r)
        left = int(left * r)
        # draw the predicted name on the image
        cv2.rectangle(frame, (left, top), (right, bottom),
            (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
            0.75, (0, 255, 0), 2)
    # ----------

    # cv2.imshow("OpenCV", frame)
    i += 1
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
# vs.stop()
mytime = time.time() - start_time
print("avg fps is: ", 1/(mytime/i))
