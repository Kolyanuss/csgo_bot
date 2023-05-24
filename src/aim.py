from windmouse import wind_mouse
import mouse
import time
import ctypes

def sleep_milliseconds(milliseconds):
    # Виклик функції time.sleep() з модуля kernel32
    ctypes.windll.kernel32.Sleep(milliseconds)


def mouse_move_to(x,y):
    mouse.move(x, y)
    sleep_milliseconds(1) # не працює нище 10мс
    
def aim(target_x,target_y):
    start_time = time.time()
    # Отримання поточного положення курсора
    current_x, current_y = mouse.get_position()
    print("Поточне положення курсора:", current_x, current_y)
    
    # Пересування курсора до нових координат з використанням алгоритму windmouse
    wind_mouse(current_x,current_y,target_x,target_y,move_mouse=mouse_move_to)

    # Отримання оновленого положення курсора
    updated_x, updated_y = mouse.get_position()
    print("Оновлене положення курсора:", updated_x, updated_y)
    
    execution_time = time.time() - start_time
    print("----Час прицілювання: ", execution_time, "секунд")

