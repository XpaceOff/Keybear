from kb import KMKKeyboard

from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.holdtap import HoldTap
from kmk.modules.split import Split, SplitSide, SplitType
from kmk.modules.encoder import EncoderHandler
from kmk.modules.cg_swap import CgSwap
from kmk.extensions.rgb import RGB

keyboard = KMKKeyboard()

# keyboard.debug_enabled = True

# TODO Comment one of these on each side
# split_side = SplitSide.LEFT
# split_side = SplitSide.RIGHT
split = Split(
    split_flip=True,
    split_type=SplitType.UART,
    # split_side=split_side,
    data_pin=keyboard.data_pin,
    use_pio=True,
)
keyboard.modules.append(split)

# HoldTap and Layers
holdtap = HoldTap()
keyboard.modules.append(holdtap)
keyboard.modules.append(Layers())

encoder_handler = EncoderHandler()
encoder_handler.pins = ((keyboard.encoder_pin_a, keyboard.encoder_pin_b, None, False),)

# GUI Swap
cg_swap = CgSwap()
keyboard.modules.append(cg_swap)

# Adding extensions
rgb = RGB(pixel_pin=keyboard.rgb_pixel_pin, num_pixels=29, hue_default=190, val_default=75)
keyboard.extensions.append(rgb)

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO
TBD_KEY = KC.NO # This key will be removed next hardware update.

DFT_L = KC.TO(0)                    # Default Layer: set default layer. 
DFT_LS = KC.HT(KC.TO(0), KC.LSFT)   # Default Layer&Shift: Shift when pressed, and set default layer when tapped.
LRS_LS = KC.HT(KC.TG(1), KC.LSFT)   # Lower Layer&Shift: Shift when pressed, and set lower layer when tapped.
RSE_L = KC.MO(2)                    # Raise Layer: set raise layer when pressed.
CFG_L = KC.MO(3)                    # Config Layer: set config layer when pressed.

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
# TODO: Delete and clean anything related to TBD_KEY
# TODO: The KC.CG_TOGG is temporary. I should move it to the config layer
keyboard.keymap = [
    [ # DEFAULT LAYER
        KC.TAB,    KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,                KC.Y,    KC.U,    KC.I,    KC.O,     KC.P,    KC.BSPC,\
        KC.CLCK,   KC.A,    KC.S,    KC.D,    KC.F,    KC.G,                KC.H,    KC.J,    KC.K,    KC.L,     KC.SCLN, KC.QUOT,\
        KC.LSFT,   KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,                KC.N,    KC.M,    KC.COMM, KC.DOT,   KC.SLSH, KC.ESC,\
        KC.LGUI,   KC.LCTL, LRS_LS,  KC.SPC,  TBD_KEY, ENC_LB0,             ENC_RB0, TBD_KEY, KC.ENTER,RSE_L,    KC.RALT, KC.X,
    ],
    [ # LOWER LAYER
        KC.TAB,    KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,               KC.N6,   KC.N7,   KC.N8,   KC.N9,    KC.N0,   KC.BSPC,\
        _______,   _______, _______, _______, _______, _______,             KC.LEFT, KC.DOWN, KC.UP,   KC.RIGHT, _______, _______,\
        _______,   _______, _______, _______, _______, _______,             _______, _______, _______, _______,  _______, _______,\
        _______,   _______, DFT_LS,  _______, TBD_KEY, ENC_LB1,             ENC_RB0, TBD_KEY, _______, DFT_L,    _______, KC.X,
    ],
    [ # RAISE LAYER
        KC.TILD,   KC.EXLM, KC.AT,   KC.HASH, KC.DLR,  KC.PERC,             KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN,  KC.RPRN, KC.BSPC,\
        _______,   _______, _______, _______, _______, _______,             KC.MINS, KC.EQL,  KC.LBRC, KC.RBRC,  KC.BSLS, KC.GRV,\
        _______,   _______, _______, _______, _______, _______,             KC.UNDS, KC.PLUS, KC.LCBR, KC.RCBR,  KC.PIPE, KC.TILD,\
        _______,   _______, CFG_L,   _______, TBD_KEY, KC.CG_TOGG,          ENC_RB0, TBD_KEY, _______, XXXXXXX,  _______, KC.X,
    ],
    [ # CONFIG LAYER
        _______,   _______, _______, _______, _______, _______,             _______, _______, _______, _______,  _______, _______,\
        _______,   _______, RGB_HI,  RGB_SI,  RGB_BI,  _______,             RGB_PFX, RGB_BFX, RGB_RFX, RGB_KFX,  RGB_SFX, _______,\
        _______,   _______, RGB_HD,  RGB_SD,  RGB_BD,  RGB_TG,              RGB_TG,  _______, _______, _______,  _______, _______,\
        _______,   _______, XXXXXXX, _______, TBD_KEY, KC.CG_TOGG,          _______, _______, _______, _______,  _______, _______,\
    ]
]

encoder_handler.map = (
    ((KC.UP, KC.DOWN),),
)
keyboard.modules.append(encoder_handler)

if __name__ == '__main__':
    keyboard.go()
