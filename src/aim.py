from windmouse import wind_mouse
import pyautogui

def mouse_move_to(x,y):
    pyautogui.moveTo(x, y)
    
def aim(target_x,target_y):
    # Отримання поточного положення курсора
    current_x, current_y = pyautogui.position()
    print("Поточне положення курсора:", current_x, current_y)
    
    # Пересування курсора до нових координат з використанням алгоритму windmouse
    wind_mouse(current_x,current_y,target_x,target_y,move_mouse=mouse_move_to)

    # Отримання оновленого положення курсора
    updated_x, updated_y = pyautogui.position()
    print("Оновлене положення курсора:", updated_x, updated_y)

