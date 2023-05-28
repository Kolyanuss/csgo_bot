from windmouse import wind_mouse
import mouse
import time
import ctypes
import win32api, win32con

def sleep_milliseconds(milliseconds):
    # Виклик функції time.sleep() з модуля kernel32
    ctypes.windll.kernel32.Sleep(milliseconds)

def move_relative(x, y):
        """move the mouse to the specified coordinates"""
        current_x, current_y = mouse.get_position()
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x-current_x, y-current_y, 0, 0)

def move_absolute(x,y):
    mouse.move(x, y)    
    # sleep_milliseconds(1) # не працює нижче 10мс
    
def aim(target_x,target_y):
    # start_time = time.time()
    # Отримання поточного положення курсора
    current_x, current_y = mouse.get_position()
    target_x,target_y = int(target_x),int(target_y)
    print("FROM", current_x, current_y,"->",target_x,target_y)
    
    # Пересування курсора до нових координат з використанням алгоритму windmouse
    wind_mouse(current_x,current_y,target_x,target_y,
               move_mouse=move_relative)
    # move_relative(target_x,target_y)

    # Отримання оновленого положення курсора
    updated_x, updated_y = mouse.get_position()
    print("res:", updated_x, updated_y)
    
    # execution_time = time.time() - start_time
    # print("Aim time: {:.4f}".format(execution_time), "sec")

def shoot():
    mouse.click()