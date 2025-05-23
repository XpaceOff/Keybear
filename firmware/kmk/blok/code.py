from kb import KMKKeyboard

from kmk.keys import KC
from kmk.modules.layers import Layers as _Layers
from kmk.modules.holdtap import HoldTap, HoldTapRepeat
from kmk.modules.split import Split, SplitSide, SplitType
from kmk.modules.encoder import EncoderHandler
from kmk.modules.cg_swap import CgSwap as _CgSwap
from kmk.modules.dynamic_sequences import DynamicSequences
from kmk.extensions.rgb import RGB
from kmk.extensions.lock_status import LockStatus
from kmk.modules.mouse_keys import MouseKeys

# Some local variables
n_key_layer = 13          # LED position of the Layer key
n_key_cgui = 21           # LED position of the GUI/Windows key
n_key_capslock = 26       # LED position of the Capslock key 
rec_max_time = 60 * 1000  # Record max time (1 minute)
cgui_hue_vals = [220, 15] # Hue values when cgswap is disabled/enabled [win/lin, mac]

keyboard = KMKKeyboard()

# Debug Mode
keyboard.debug_enabled = False

# TODO: Comment one of these on each side
# split_side = SplitSide.LEFT
# split_side = SplitSide.RIGHT
split = Split(
    split_flip=True, # If both halves are the same, but flipped, set this True
    # split_side=split_side, # Sets if this is to SplitSide.LEFT or SplitSide.RIGHT, or use EE hands
    split_type=SplitType.UART, # Defaults to UART
    split_target_left=True,  # Assumes that left will be the one on USB. Set to False if it will be the right
    uart_interval=20, # Sets the uarts delay. Lower numbers draw more power
    data_pin=keyboard.data_pin_rx, # The primary data pin to talk to the secondary device with
    data_pin2=keyboard.data_pin_tx, # Second uart pin to allow 2 way communication
    uart_flip=True, # Reverses the RX and TX pins if both are provided
    use_pio=True,
)

# Adding RGB extension
rgb = RGB(pixel_pin=keyboard.rgb_pixel_pin, num_pixels=28, hue_default=190, val_default=75)
keyboard.extensions.append(rgb)

class Layers(_Layers):
    first_boot = True # True when keyboard first boot
    last_top_layer = 0 # Stores the last active layer
    hues = (10, 20, 69, 100, 180, 250, 35)

    def after_hid_send(self, keyboard):
        # In the LOWER layer, I have numbers and arrow keys.
        # When LOWER layer is selected, I would like go back 
        # to the DEFAULT layer if a-z or ENTER keys are pressed
        if keyboard.active_layers[0] == 1:
            for nkey in keyboard.keys_pressed:
                if nkey.code >= 4 and nkey.code <= 29 or nkey.code == 40:
                    # This is the code for KC.TO(layer)
                    self._active_combo = None
                    keyboard.active_layers.clear()
                    keyboard.active_layers.insert(0, 0)
                    break

        # This is the code that updates the color of the "layer button"
        # This code will be executed when the active layer changes OR when the keyboard first boots up
        if keyboard.active_layers[0] != self.last_top_layer or self.first_boot:
            self.first_boot = False
            self.last_top_layer = keyboard.active_layers[0]
            rgb.set_hsv(self.hues[self.last_top_layer], 255, rgb.val, n_key_layer)
            rgb.show()

keyboard.modules.append(Layers())

# React to Lock Status
class LEDLockStatus(LockStatus):
    first_boot = True # True when keyboard first boot
    def set_lock_leds(self):
        if self.get_caps_lock():
            rgb.set_hsv(100, 255, rgb.val, n_key_capslock)
        else:
            rgb.set_hsv(0, 0, 0, n_key_capslock)
        rgb.show()

    def after_hid_send(self, sandbox):
        if self.first_boot:
            self.set_lock_leds()
            self.first_boot = False

        super().after_hid_send(sandbox)  # Critically important. Do not forget
        if self.report_updated:
            self.set_lock_leds()

keyboard.extensions.append(LEDLockStatus())

# GUI Swap
class CgSwap(_CgSwap):
    last_swap_state = False
    first_boot = True

    def after_hid_send(self, keyboard):
        if self.last_swap_state != self.cg_swap_enable or self.first_boot:
            self.last_swap_state = self.cg_swap_enable
            self.first_boot = False

            this_hue = cgui_hue_vals[0]
            if self.cg_swap_enable == True:
                this_hue = cgui_hue_vals[1]

            rgb.set_hsv(this_hue, 255, rgb.val, n_key_cgui)
            rgb.show()

cg_swap = CgSwap()
keyboard.modules.append(cg_swap)

# HoldTap
holdtap = HoldTap()
keyboard.modules.append(holdtap)

# NOTE: For some reason Split needs to added after HoldTap
keyboard.modules.append(split)

# Encoder
encoder_handler = EncoderHandler()
encoder_handler.pins = ((keyboard.encoder_pin_a, keyboard.encoder_pin_b, None, False),)

# Record a sequence of keys.
dynamicSequences = DynamicSequences(
    timeout=rec_max_time, # Max time record. ms
    # use_recorded_speed = True
)

keyboard.modules.append(dynamicSequences)
RECORD = KC.RECORD_SEQUENCE()
REC_STP = KC.STOP_SEQUENCE()
REC_PLY = KC.PLAY_SEQUENCE()

keyboard.modules.append(MouseKeys())

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

DFT_L = KC.TO(0)                    # Default Layer: set default layer. 
DFT_LS = KC.HT(KC.TO(0), KC.LSFT)   # Default Layer&Shift: Shift when pressed, and set default layer when tapped.
LRS_LS = KC.HT(KC.TG(1), KC.LSFT)   # Lower Layer&Shift: Shift when pressed, and set lower layer when tapped.
RSE_L = KC.MO(2)                    # Raise Layer: set raise layer when pressed.
RD_LL = KC.HT(KC.TO(0), KC.MO(2))   # Raise & Default Layers: Set default layer when tapped, and set raise layer when pressed.
CFG_L = KC.MO(3)                    # Config Layer: set config layer when pressed.
FUC_L = KC.MO(4)                    # Function Layer: set function layer when pressed
ARW_LE = KC.HT(KC.ENTER, KC.MO(5))
KYP_LC = KC.HT(KC.CAPS, KC.MO(6))

ALT_L = KC.RALT(KC.LEFT)
ALT_R = KC.RALT(KC.RIGHT)
ALT_U = KC.RALT(KC.UP)
ALT_D = KC.RALT(KC.DOWN)

RGB_TG = KC.RGB_TOG # Turn ON/OFF RGB.
RGB_BI = KC.RGB_VAI # + Brightness
RGB_BD = KC.RGB_VAD # - Brightness
RGB_SI = KC.RGB_SAI # + Saturation
RGB_SD = KC.RGB_SAD # - Saturation
RGB_HI = KC.RGB_HUI # + Hue
RGB_HD = KC.RGB_HUD # - Hue
RGB_PFX = KC.RGB_MODE_PLAIN
RGB_BFX = KC.RGB_MODE_BREATHE
RGB_RFX = KC.RGB_MODE_RAINBOW
RGB_KFX = KC.RGB_MODE_KNIGHT
RGB_SFX = KC.RGB_MODE_SWIRL

ENC_LB0 = KC.RGB_MODE_SWIRL # Encoder Left Button
ENC_LB1 = KC.RGB_VAD        # Encoder Left Button
ENC_RB0 = KC.RGB_HUI        # Encoder Right Button

# TODO: Update the 'ENC` encoder keys
# TODO: The KC.CG_TOGG is temporary. I should move it to the config layer
keyboard.keymap = [
    [ # DEFAULT LAYER
        KC.TAB,    KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,                KC.Y,    KC.U,    KC.I,    KC.O,     KC.P,    KC.BSPC,\
        KYP_LC,    KC.A,    KC.S,    KC.D,    KC.F,    KC.G,                KC.H,    KC.J,    KC.K,    KC.L,     KC.SCLN, KC.QUOT,\
        KC.LSFT,   KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,                KC.N,    KC.M,    KC.COMM, KC.DOT,   KC.SLSH, KC.ESC,\
                   KC.LGUI, KC.LCTL, LRS_LS,  KC.SPACE,ENC_LB0,             ENC_RB0, ARW_LE,  RSE_L,   KC.RALT,  FUC_L,
    ],
    [ # LOWER LAYER
        _______,   KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,               KC.N6,   KC.N7,   KC.N8,   KC.N9,    KC.N0,   _______,\
        _______,   _______, _______, _______, _______, _______,             KC.LEFT, KC.DOWN, KC.UP,   KC.RIGHT, _______, _______,\
        _______,   _______, _______, _______, _______, _______,             _______, _______, _______, _______,  _______, _______,\
                   _______, _______, DFT_LS,  _______, ENC_LB1,             ENC_RB0, _______, RD_LL,   _______,  _______,
    ],
    [ # RAISE LAYER
        KC.TILD,   KC.EXLM, KC.AT,   KC.HASH, KC.DLR,  KC.PERC,             KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN,  KC.RPRN, _______,\
        _______,   _______, _______, RECORD,  REC_STP, REC_PLY,             KC.MINS, KC.EQL,  KC.LBRC, KC.RBRC,  KC.BSLS, KC.GRV,\
        _______,   _______, _______, _______, _______, _______,             KC.UNDS, KC.PLUS, KC.LCBR, KC.RCBR,  KC.PIPE, KC.TILD,\
                   _______, _______, CFG_L,   _______, KC.CG_TOGG,          ENC_RB0, _______, XXXXXXX, _______,  _______,
    ],
    [ # CONFIG LAYER
        _______,   _______, _______, _______, KC.RESET,_______,             _______, _______, _______, _______,  _______, _______,\
        _______,   _______, _______, RGB_SI,  RGB_HI,  RGB_BI,              RGB_PFX, RGB_BFX, RGB_RFX, RGB_KFX,  RGB_SFX, _______,\
        _______,   _______, _______, RGB_SD,  RGB_HD,  RGB_BD,              RGB_TG,  _______, _______, _______,  _______, _______,\
                   _______, _______, XXXXXXX, _______, KC.CG_TOGG,          _______, _______, _______, _______,  _______,\
    ],
    [ # FUNCTION LAYER
        _______,   KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,               KC.F6,   KC.F7,   KC.F8,   KC.F9,    KC.F10,  KC.DELETE,\
        _______,   _______, _______, _______, _______, _______,             _______, _______, _______, _______,  _______, _______,\
        _______,   _______, _______, _______, _______, _______,             _______, _______, _______, _______,  _______, _______,\
                   _______, _______, _______, _______, _______,             _______, _______, _______, _______,  _______,\
    ],
    [ # ARROW LAYER, NOTE: This might replace the LOWER layer
        _______,    KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,              KC.N6,   KC.N7,   KC.N8,   KC.N9,    KC.N0,   _______,\
        _______,   _______, _______, _______, _______, _______,             KC.LEFT, KC.DOWN, KC.UP,   KC.RIGHT, _______, _______,\
        _______,   _______, _______, _______, _______, _______,             ALT_L,   ALT_D,   ALT_U,   ALT_R,    _______, _______,\
                   _______, _______, _______, _______, _______,             _______, _______, _______, _______,  _______,\
    ],
    [ # KEYPAD LAYER
        _______,   _______, _______, _______, _______, _______,             KC.N7,   KC.N8,   KC.N9,   XXXXXXX,  XXXXXXX, _______,\
        _______,   _______, _______, _______, _______, _______,             KC.N4,   KC.N5,   KC.N6,   XXXXXXX,  XXXXXXX, XXXXXXX,\
        _______,   _______, _______, _______, _______, _______,             KC.N1,   KC.N2,   KC.N3,   KC.DOT,   XXXXXXX, XXXXXXX,\
                   _______, _______, _______, _______, _______,             XXXXXXX, XXXXXXX, KC.N0,   XXXXXXX,  XXXXXXX,\
    ]
]

encoder_handler.map = (
    ((KC.MW_UP, KC.MW_DOWN),),
)
keyboard.modules.append(encoder_handler)

if __name__ == '__main__':
    keyboard.go()
