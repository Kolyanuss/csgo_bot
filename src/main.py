import cv2
import math
import dxcam
import threading
from pynput.keyboard import Key, Listener as KeyListener
import detector
import aim
from custom_sleep import sleep

ACTIVE_MODE = True
AIM_MODE = False
PRINT_MODE = False
DRAW_MODE = True
# shift = 26 # зсув на 26 пікслеів нище щоб не записувати верхню рамку вікна
# monitor = (0, shift, 1024, 768+shift)
screen_resolution = (1920, 1080)
mid_screen = (int(screen_resolution[0]/2), int(screen_resolution[1]/2))
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
    min_x = min(x1, x2)
    max_x = max(x1, x2)
    min_y = min(y1, y2)
    max_y = max(y1, y2)
    
    if min_x <= x <= max_x and min_y <= y <= max_y:
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
            point = detector.get_closest_object(results.xyxy[0].cpu().numpy())
            if point is not None:
                # x1,y1 = aim.my_mouse.get_position()
                rectangle = (int(point[0]),int(point[1]),int(point[2]),int(point[3]))
                if is_cursor_inside_box(*mid_screen,*cut_rectangle(rectangle)):
                    aim.shoot()
                    sleep(0.1)
                else:
                    aim.aim(*detector._get_center_point(*rectangle))
                # AIM_MODE = False

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