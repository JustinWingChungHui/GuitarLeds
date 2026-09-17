from gpiozero import Button
from signal import pause
import subprocess

BUTTON_PIN = 17
NORMAL_SCRIPT = "/home/justin/change_effect.sh"
LOUD_SCRIPT = "/home/justin/change_effect_loud.sh"

loud = [False]

button = Button(BUTTON_PIN, bounce_time=0.1)  # 100ms debounce

def on_press():
    if loud[0]:
        subprocess.run([LOUD_SCRIPT])
    else:
        subprocess.run([NORMAL_SCRIPT])

    loud[0] = not loud[0]

def on_release():
    subprocess.run([RELEASE_SCRIPT])

button.when_pressed = on_press
# button.when_released = on_release

pause()