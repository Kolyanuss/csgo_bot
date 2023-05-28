from windmouse import wind_mouse
import mouse
import time
import ctypes
import win32api, win32con
from MouseControls import MouseControls

my_mouse = MouseControls()

def sleep_milliseconds(milliseconds):
    # Виклик функції time.sleep() з модуля kernel32
    ctypes.windll.kernel32.Sleep(milliseconds)

def move_relative(x, y):
    current_x, current_y = my_mouse.get_position()
    # my_mouse.move_relative(int((x-current_x)*0.774), int((y-current_y)*0.774))
    my_mouse.move_relative(int((x-current_x)*1.2), int((y-current_y)*1.2))

 
def aim(target_x,target_y):
    # start_time = time.time()
    # Отримання поточного положення курсора
    current_x, current_y = my_mouse.get_position()
    target_x,target_y = int(target_x),int(target_y)
    print("FROM", current_x, current_y,"->",target_x,target_y)
    
    # Пересування курсора до нових координат з використанням алгоритму windmouse
    # wind_mouse(current_x,current_y,target_x,target_y,
    #            move_mouse=my_mouse.move)
    move_relative(target_x,target_y)
    # my_mouse.move(target_x,target_y)

    # Отримання оновленого положення курсора
    print("res:", my_mouse.get_position())
    
    # execution_time = time.time() - start_time
    # print("Aim time: {:.4f}".format(execution_time), "sec")

def shoot():
    my_mouse.click()