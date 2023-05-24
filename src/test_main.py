from pynput.mouse import Listener
import aim

def on_click(x, y, button, pressed):
    if button == button.left and pressed:
        print("Ліва кнопка миші натиснута.")
        aim.aim(1000,500)
        return False

with Listener(on_click=on_click) as listener:
    listener.join()

