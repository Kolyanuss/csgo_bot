import cv2
import math
import dxcam
import threading
from pynput.keyboard import Key, Listener as KeyListener
import detector
import aim
from custom_sleep import sleep

ACTIVE_MODE = True
AIM_MODE = True
DRAW_MODE = True
# shift = 26 # зсув на 26 пікслеів нище щоб не записувати верхню рамку вікна (якщо віконний режим)
# monitor = (0, shift, 1024, 768+shift)
screen_resolution = (1920, 1080)
mid_screen_xy = (int(screen_resolution[0]/2), int(screen_resolution[1]/2))
monitor = (0, 0, *screen_resolution)
camera = dxcam.create()
threshold = 10 # maximum deviation for a shot

def on_press(key):
    global ACTIVE_MODE
    if key == Key.home and ACTIVE_MODE != True:
        ACTIVE_MODE = True
        thread = threading.Thread(target=main)
        thread.start()
    if key == Key.end:
        ACTIVE_MODE = False
    global AIM_MODE
    if key == Key.shift_l and AIM_MODE != True:
        AIM_MODE = True
        print("AIM MODE: ",AIM_MODE)
    if key == Key.alt_l:
        AIM_MODE = False
        print("AIM MODE: ",AIM_MODE)
    if key == Key.delete:
        return False

def start_listener():
    with KeyListener(on_press=on_press) as listener:
        thread = threading.Thread(target=main)
        thread.start()
        listener.join()

def is_cursor_inside_box(x, y, x1, y1, x2, y2):
    if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
        return True
    else:
        return False

def cut_rectangle(rect,by=1.3):
    x1,y1,x2,y2 = rect
    width = abs(x1-x2)
    height = abs(y1-y2)
    new_width = width/by
    new_height = height/1.1

    new_x1 = x1+(new_width/2)
    new_y1 = y1+(new_height/2)
    new_x2 = x2-(new_width/2)
    new_y2 = y2-(new_height/2)
    new_rect = (new_x1,new_y1,new_x2,new_y2)

    return new_rect

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
            box = detector.get_closest_object(results)
            if box is not None:
                if is_cursor_inside_box(*mid_screen_xy,*cut_rectangle(box)):
                    aim.shoot()
                    sleep(0.11)
                    aim.shoot()
                    sleep(0.1)
                else:
                    aim.aim(*detector._get_center_point(*box))
                    sleep(0.01)
                # AIM_MODE = False
        
        global DRAW_MODE
        if DRAW_MODE:
            # draw boxes in other window
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            detector.new_draw_detection(frame,results)
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