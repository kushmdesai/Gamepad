import board
from arrows import Karrows
from kmk.keys import KC
from kmk.modules.combos import Combos, Chord
from kmk.modules.mouse_keys import MouseKeys
from kmk.modules.layers import Layers

keyboard = Karrows()

# --- Modules ---
layers = Layers()
keyboard.modules.append(layers)

# LEFT + RIGHT together toggles layer 1 on/off.
# Individually, LEFT and RIGHT still work normally as defined below.
# NOTE: the combo list must be passed into Combos() here directly -
# the module reads its own self.combos, it does not read keyboard.combos.
combos = Combos(combos=[
    Chord((KC.LEFT, KC.RIGHT), KC.TG(1)),
])
keyboard.modules.append(combos)

mouse_keys = MouseKeys()
keyboard.modules.append(mouse_keys)

# --- Keymap ---
# Matrix order confirmed from the deployed code.py: index 0=RIGHT, 1=LEFT, 2=DOWN, 3=UP
keyboard.keymap = [
    # Layer 0 (default) - arrow keys, unchanged
    [KC.RIGHT, KC.LEFT, KC.DOWN, KC.UP],

    # Layer 1 - shortcuts
    # RIGHT -> cmd-tab
    # LEFT  -> cmd+w
    # DOWN  -> cmd+shift+t
    # UP    -> left click
    [KC.LGUI(KC.TAB), KC.LGUI(KC.W), KC.LGUI(KC.LSFT(KC.T)), KC.MB_LMB],
]

# --- Debug prints ---
# This KMK version has no on_key_press/on_key_release decorators, so we
# wrap the real process_key method instead to log every key event.
_original_process_key = keyboard.process_key

def _debug_process_key(key, is_pressed, int_coord=None):
    print("key={} is_pressed={} int_coord={} active_layers={}".format(
        key, is_pressed, int_coord, keyboard.active_layers
    ))
    return _original_process_key(key, is_pressed, int_coord)

keyboard.process_key = _debug_process_key

print("Keyboard booting...")
print("Keymap layers loaded: {}".format(len(keyboard.keymap)))
print("Combos configured: {}".format(len(combos.combos)))

if __name__ == '__main__':
    keyboard.go()
