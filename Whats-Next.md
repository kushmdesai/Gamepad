
---

# 🛠️ What I'm Building

A 4-key macroboard using:

* **Seeed XIAO RP2040**
* **4 buttons** (GP0–GP3)
* **2 SK6812 MINI-E LEDs** (data on GP4)
* **KMK firmware** with custom rainbow + reactive lighting

---
## What I'll do after I get The parts
### ✅ Step 1: Install CircuitPython

1. **Download the CircuitPython UF2 for XIAO RP2040:**

   * Visit [https://circuitpython.org/board/seeed\_xiao\_rp2040/](https://circuitpython.org/board/seeed_xiao_rp2040/)
   * Download the `.uf2` file

2. **Put the board into bootloader mode:**

   * Hold the **boot button** on the XIAO RP2040
   * Plug it into USB
   * It will mount as `RPI-RP2`

3. **Drag and drop the UF2 file** onto `RPI-RP2`

4. The board will reboot and mount as `CIRCUITPY`

---

### ✅ Step 2: Download and Install KMK

1. Download KMK:

   * Go to: [https://github.com/KMKfw/kmk\_firmware](https://github.com/KMKfw/kmk_firmware)
   * Click **Code > Download ZIP**
   * Unzip it

2. Copy these to my `CIRCUITPY/lib/` folder:

   * From `kmk_firmware/`:

     * Copy the whole `kmk/` folder into `CIRCUITPY/lib/`

---

### ✅ Step 3: Install Required Libraries

I also need some dependencies from Adafruit:

1. Go to [https://circuitpython.org/libraries](https://circuitpython.org/libraries)

   * Download the **latest library bundle** (e.g., `adafruit-circuitpython-bundle-*.zip`)

2. Extract the ZIP, and go into `lib/`

3. Copy these files to my `CIRCUITPY/lib/`:

   * `adafruit_pixelbuf.mpy`
   * `neopixel.mpy`

Now my `CIRCUITPY/lib/` should have:

```
lib/
├── kmk/
├── adafruit_pixelbuf.mpy
├── neopixel.mpy
```

---

### ✅ Step 4: Add my Firmware Code

1. Create a file called `code.py` on the `CIRCUITPY` drive

2. Paste in this full working code:

```python
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
```

💾 Save the file — my board will **auto-reload** and start running it.

---

### ✅ Step 5: Test It!

* Press each button → the corresponding LED flashes a color
* Let go → rainbow pulse resumes
* Connect to PC: KMK should act like a USB keyboard

---

### ✅ Optional: Debugging

If something doesn’t work:

1. Open **Mu Editor**, **Thonny**, or **Arduino Serial Monitor**
2. Select the **CIRCUITPY USB COM port**
3. Check for errors or typos in the REPL

---

### 🧪 Whats Next?

* Make a full Keyboard
* Rgb keys on the Keyboard
* Mechanical Keys
* Use matrix insted of wiring each key idividually
* Switch animations with a key

---