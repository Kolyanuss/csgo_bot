from windmouse import wind_mouse
import ctypes
from MouseControls import MouseControls
# from screen_to_world import get_move_angle

screen_resolution = (1920, 1080)
mid_screen_xy = (int(screen_resolution[0]/2), int(screen_resolution[1]/2))
my_mouse = MouseControls()

def sleep_milliseconds(milliseconds):
    # Виклик функції time.sleep() з модуля kernel32
    ctypes.windll.kernel32.Sleep(milliseconds)

def move_relative(x, y):
    # current_x, current_y = my_mouse.get_position()
    my_mouse.move_relative(int((x-mid_screen_xy[0])*0.9), int((y-mid_screen_xy[1])*0.9))

 
def aim2(target_x,target_y):
    target_x,target_y = int(target_x),int(target_y)
    print("To: ",target_x,target_y)
    
    # Пересування курсора до нових координат з використанням алгоритму windmouse
    wind_mouse(mid_screen_xy[0], mid_screen_xy[1], target_x, target_y,
               move_mouse=move_relative)    

    # Отримання оновленого положення курсора
    print("res:", my_mouse.get_position())

# stable
def aim(target_x,target_y):
    # start_time = time.time()
    # Отримання поточного положення курсора
    target_x,target_y = int(target_x),int(target_y)
    print("To: ",target_x,target_y)
    
    # Пересування курсора до нових координат
    move_relative(target_x,target_y)

    # Отримання оновленого положення курсора
    print("res:", my_mouse.get_position())
    
    # execution_time = time.time() - start_time
    # print("Aim time: {:.4f}".format(execution_time), "sec")

def shoot():
    my_mouse.click()