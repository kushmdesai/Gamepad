import board
import digitalio
import storage

# Same 4 pins used by the macropad matrix in arrows.py (D9=RIGHT, D10=LEFT, D7=DOWN, D8=UP)
pins = (board.D9, board.D10, board.D7, board.D8)

buttons = []
for pin in pins:
    io = digitalio.DigitalInOut(pin)
    io.pull = digitalio.Pull.UP
    buttons.append(io)

# value_when_pressed=False in arrows.py means each pin reads False when pressed
all_pressed = all(not b.value for b in buttons)

if not all_pressed:
    # Not all 4 keys held at boot -> hide the CIRCUITPY drive,
    # board boots straight into keyboard/HID mode only.
    storage.disable_usb_drive()

# Release the pins so code.py's matrix scanner can use them normally
for b in buttons:
    b.deinit()
