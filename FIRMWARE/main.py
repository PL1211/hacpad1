import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.rgb import RGB
from kmk.extensions.media_keys import MediaKeys

# Initialize Keyboard
keyboard = KMKKeyboard()

# --- Extensions ---
# Enable Media Keys (for Volume/Mute/Play)
keyboard.extensions.append(MediaKeys())

# Enable RGB (SK6812 LEDs)
# Pin D9 (GPIO4) matches Pin 10 on the schematic for LED Data
rgb = RGB(
    pixel_pin=board.D9,
    num_pixels=6,
    val_limit=255,
    hue_default=0,
    sat_default=255,
    val_default=100,
)
keyboard.extensions.append(rgb)

# --- Encoder Setup ---
encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

# Encoder Pins: Pin 7 (D6/TX) & Pin 8 (D7/RX)
# 3rd element is None (no switch defined), 4th is False (assume internal pullups/conditioning)
encoder_handler.pins = ((board.D6, board.D7, None, False),)

# Encoder Map: Rotate for LED Brightness (Value Increase/Decrease)
# Layer 0
encoder_handler.map = [
    ((KC.RGB_VAI, KC.RGB_VAD),), # Clockwise: Brightness Up, Counter-CW: Brightness Down
]

# --- Button Pins ---
# Matches schematic: SW1=D0, SW2=D1, SW3=D2, SW4=D3, SW5=D4, SW6=D5
PINS = [board.D0, board.D1, board.D2, board.D3, board.D4, board.D5]

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False, # Assumes switches connect to GND (internal pullup)
)

# --- Keymap ---
# 1. Play/Pause
# 2. Vol Up
# 3. Vol Down
# 4. Mute
# 5. LED Toggle (Off/On)
# 6. LED Mode (Cycle Effects) - Used as "On" alternative or to change patterns
keyboard.keymap = [
    [
        KC.MPLY,      # SW1: Play/Pause
        KC.VOLU,      # SW2: Volume Up
        KC.VOLD,      # SW3: Volume Down
        KC.MUTE,      # SW4: Mute
        KC.RGB_TOG,   # SW5: LED Off (Toggle)
        KC.RGB_M_P,   # SW6: LED On/Mode (Switches to "Plain" static color mode)
    ]
]

if __name__ == '__main__':
    keyboard.go()
