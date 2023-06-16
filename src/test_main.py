from pynput.mouse import Listener
import aim

def on_click(x,y,button, pressed):
    if button == button.right and pressed:
        # print("Ліва кнопка миші натиснута.")
        # aim.aim(960+960,540)
        aim.aim(1920,540)
    else: return False

with Listener(on_click=on_click) as listener:
    listener.join()

