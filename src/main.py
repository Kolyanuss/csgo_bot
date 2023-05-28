import cv2
import dxcam
import detector
import threading
from pynput.keyboard import Key, Listener as KeyListener
import aim

ACTIVE_MODE = True
AIM_MODE = False
PRINT_MODE = False
DRAW_MODE = True
# shift = 26 # зсув на 26 пікслеів нище щоб не записувати верхню рамку вікна
# monitor = (0, shift, 1024, 768+shift)
shift = 0 # зсув на 26 пікслеів нище щоб не записувати верхню рамку вікна
monitor = (0, 0, 1920, 1080)
camera = dxcam.create()


def on_press(key):
    global ACTIVE_MODE
    if key == Key.home and ACTIVE_MODE != True:
        ACTIVE_MODE = True
        thread = threading.Thread(target=main)
        thread.start()
    if key == Key.end:
        ACTIVE_MODE = False
    global AIM_MODE
    if key == Key.page_up and AIM_MODE != True:
        AIM_MODE = True
        print("AIM MODE: ",AIM_MODE)
    if key == Key.page_down:
        AIM_MODE = False
        print("AIM MODE: ",AIM_MODE)
    if key == Key.f1:
        return False

def start_listener():
    with KeyListener(on_press=on_press) as listener:
        thread = threading.Thread(target=main)
        thread.start()
        listener.join()


def main():
    camera.start(region=monitor)
    global ACTIVE_MODE
    print("Start capture")
    while ACTIVE_MODE:
        # take screen shot
        frame = camera.get_latest_frame()
        # show img to model and get result
        results = detector.detect(frame)

        # AIM section
        global AIM_MODE
        if AIM_MODE:
            point = detector.get_big_detect_mid_point(results.xyxy[0].cpu().numpy())
            if point:
                aim.aim(point[0],point[1]+shift)
                aim.shoot()
                AIM_MODE = False


        # info in console (optional)
        if PRINT_MODE:
            results.print()
        
        global DRAW_MODE
        if DRAW_MODE:
            # draw boxes in other window
            detector.draw_detection(frame, results.xyxy[0].cpu().numpy())
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)           
            frame = cv2.resize(frame, (int(frame.shape[1]/2), int(frame.shape[0]/2)))
            cv2.imshow("csgo inference", frame)
            # break section
            if cv2.waitKey(1) & 0xFF == ord("q"):
                DRAW_MODE = False
                break

    print("Stop capture")
    cv2.destroyAllWindows()
    camera.stop()


print("Program STARTED")
start_listener()