import cv2
import numpy as np
import time
import mss
from multiprocessing import Queue, Process

rect = {"top": 0, "left": 0, "width": 600, "height": 500}


def grab(queue: Queue) -> None:
    with mss.mss() as sct:
        for _ in range(500):
            queue.put(np.array(sct.grab(rect)))

    # Tell the other worker to stop
    queue.put(None)


def save(queue: Queue) -> None:
    while "there are screenshots":
        img = queue.get()
        if img is None:
            break
        cv2.imshow("OpenCV/thread", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    queue: Queue = Queue()

    # 2 processes: one for grabing and one for showing img
    x1 = Process(target=grab, args=(queue,))
    x = Process(target=save, args=(queue,))
    start_time = time.time()
    x1.start()
    x.start()
    x.join()
    end_time = time.time()
    print("avg fps: ", 1/((end_time-start_time)/500))
