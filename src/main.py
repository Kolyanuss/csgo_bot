import cv2
import dxcam
import detector
import threading
from pynput.keyboard import Key, Listener as KeyListener
import aim

ACTIVE_MODE = False
PRINT_MODE = False
DRAW_MODE = True
shift = 26 # зсув на 26 пікслеів нище щоб не записувати верхню рамку вікна
monitor = (0, shift, 1024, 768+shift)
camera = dxcam.create()


def on_press(key):
    global ACTIVE_MODE
    if key == Key.home and ACTIVE_MODE != True:
        ACTIVE_MODE = True
        print("ACTIVE MODE: ",ACTIVE_MODE)
        thread = threading.Thread(target=main)
        thread.start()
    if key == Key.end:
        ACTIVE_MODE = False
        print("ACTIVE MODE: ",ACTIVE_MODE)
    if key == Key.esc:
        return False

def start_listener():
    with KeyListener(on_press=on_press) as listener:
        listener.join()


def main():
    camera.start(region=monitor)
    global ACTIVE_MODE
    print("Start capture")
    while ACTIVE_MODE:
        # take screen shot
        frame = camera.get_latest_frame()
        # resize img to yolo format
        frame = detector.convert_to_yolo_format(frame)
        # show img to model and get result
        results = detector.detect(frame)

        # AIM section
        for object in detector.get_detected_points(frame, results.xyxy[0].cpu().numpy()):
            aim.aim(object[0],object[1]+shift)

        # info in console (optional)
        if PRINT_MODE:
            results.print()
        
        global DRAW_MODE
        if DRAW_MODE:
            # draw boxes in other window
            detector.draw_detection(frame, results.xyxy[0].cpu().numpy())
            cv2.imshow("OpenCV", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))        
            # break section
            if cv2.waitKey(1) & 0xFF == ord("q"):
                DRAW_MODE = False
                break

    print("Stop capture")
    cv2.destroyAllWindows()
    camera.stop()


print("Program STARTED")
start_listener()