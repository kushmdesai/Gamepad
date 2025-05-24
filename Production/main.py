import board
import time
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import Scanner
from kmk.scanners.direct import DirectPins
from kmk.keys import KC
from kmk.extensions.rgb import RGB
from adafruit_pixelbuf import colorwheel

keyboard = KMKKeyboard()

keyboard.scanner = Scanner(DirectPins(
    pins=(board.GP0, board.GP1, board.GP2, board.GP3),
    value_when_pressed=False,
    pull=True,
))

keyboard.keymap = [
    [KC.UP, KC.LEFT, KC.RIGHT, KC.DOWN]
]

rgb = RGB(
    pixel_pin=board.GP4,
    num_pixels=2,
    val_default=40,
    animation_mode=RGB.MODE_STATIC,
)
keyboard.extensions.append(rgb)

rainbow_index = 0
flash_active = [False, False]
flash_start_time = [0.0, 0.0]
flash_duration = 0.25

flash_colors = {
    0: (255, 0, 0),     # Red
    1: (0, 255, 0),     # Green
    2: (0, 0, 255),     # Blue
    3: (255, 255, 0),   # Yellow
}

@keyboard.before_matrix_scan
def update_leds():
    global rainbow_index
    now = time.monotonic()

    for i in range(2):
        if flash_active[i]:
            if now - flash_start_time[i] < flash_duration:
                rgb.pixel(i, flash_colors.get(i, (255, 255, 255)))
            else:
                flash_active[i] = False
                rgb.pixel(i, colorwheel((rainbow_index + i * 30) % 256))
        else:
            rgb.pixel(i, colorwheel((rainbow_index + i * 30) % 256))

    rgb.show()
    rainbow_index = (rainbow_index + 1) % 256

@keyboard.on_key_press
def on_key_pressed(key):
    key_to_led = {
        0: 0,  # UP
        1: 0,  # LEFT
        2: 1,  # RIGHT
        3: 1   # DOWN
    }

    led = key_to_led.get(key.key_number)
    if led is not None:
        flash_active[led] = True
        flash_start_time[led] = time.monotonic()

if __name__ == '__main__':
    keyboard.go()
