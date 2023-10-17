from kb import KMKKeyboard

from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.holdtap import HoldTap
from kmk.modules.split import Split, SplitSide, SplitType
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.RGB import RGB

keyboard = KMKKeyboard()

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

# Adding extensions
rgb = RGB(pixel_pin=keyboard.rgb_pixel_pin, num_pixels=29, hue_default=190)
keyboard.extensions.append(rgb)

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

DFT_L = KC.TO(0) #KC.MO(1)
DFT_SL = KC.HT(KC.TO(0), KC.LSFT)#KC.MO(1)
LRS_SL = KC.HT(KC.TG(1), KC.LSFT)#KC.MO(1)
RSE_L = KC.MO(2)

ENC_LB = KC.RGB_MODE_SWIRL # Encoder Left Button
ENC_RB = KC.RGB_HUI        # Encoder Right Button

keyboard.keymap = [
    [ # DEFAULT LAYER
        KC.TAB,    KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,                KC.Y,    KC.U,    KC.I,    KC.O,     KC.P,    KC.BSPC,\
        KC.CLCK,   KC.A,    KC.S,    KC.D,    KC.F,    KC.G,                KC.H,    KC.J,    KC.K,    KC.L,     KC.SCLN, KC.QUOT,\
        KC.LSFT,   KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,                KC.N,    KC.M,    KC.COMM, KC.DOT,   KC.SLSH, KC.RSFT,\
        KC.LGUI,   KC.LCTL, LRS_SL,  KC.SPC,  KC.X,    ENC_LB,              ENC_RB,  KC.X,    KC.ENTER,RSE_L,    KC.RALT, KC.X,
    ],
    [ # LOWER LAYER
        KC.TAB,    KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,               KC.N6,   KC.N7,   KC.N8,   KC.N9,    KC.N0,   KC.BSPC,\
        KC.CLCK,   _______, _______, _______, _______, _______,             KC.LEFT, KC.DOWN, KC.UP,   KC.RIGHT, _______, _______,\
        KC.LSFT,   _______, _______, _______, _______, _______,             _______, _______, _______, _______,  _______, _______,\
        KC.LGUI,   KC.LCTL, DFT_L,   KC.SPC,  KC.X,    ENC_LB,              ENC_RB,  KC.X,    KC.ENTER,KC.X,     KC.RALT, KC.X,
    ],
    [ # RAISE LAYER
        KC.TILD,   KC.EXLM, KC.AT,   KC.HASH, KC.DLR,  KC.PERC,             KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN,  KC.RPRN, KC.BSPC,\
        KC.CLCK,   _______, _______, _______, _______, _______,             KC.MINS, KC.EQL,  KC.LBRC, KC.RBRC,  KC.BSLS, KC.GRV,\
        KC.LSFT,   _______, _______, _______, _______, _______,             KC.UNDS, KC.PLUS, KC.LCBR, KC.RCBR,  KC.PIPE, KC.TILD,\
        KC.LGUI,   KC.LCTL, DFT_L,   KC.SPC,  KC.X,    ENC_LB,              ENC_RB,  KC.X,    KC.ENTER,KC.X,     KC.RALT, KC.X,
    ]
]

encoder_handler.map = (
    ((KC.UP, KC.DOWN),),
)
keyboard.modules.append(encoder_handler)

if __name__ == '__main__':
    keyboard.go()
