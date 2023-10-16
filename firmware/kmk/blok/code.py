from kb import KMKKeyboard

from kmk.keys import KC
from kmk.modules.layers import Layers
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
keyboard.modules.append(Layers())

encoder_handler = EncoderHandler()
encoder_handler.pins = ((keyboard.encoder_pin_a, keyboard.encoder_pin_b, None, False),)

# Adding extensions
rgb = RGB(pixel_pin=keyboard.rgb_pixel_pin, num_pixels=29, hue_default=190)
keyboard.extensions.append(rgb)

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

LOWER = KC.MO(1)
RAISE = KC.MO(2)

keyboard.keymap = [
    [
        KC.TAB,    KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,                KC.Y,    KC.U,    KC.I,    KC.O,  KC.P,    KC.BSPC,\
        KC.CLCK,   KC.A,    KC.S,    KC.D,    KC.F,    KC.G,                KC.H,    KC.J,    KC.K,    KC.L,  KC.SCLN, KC.QUOT,\
        KC.LSFT,   KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,                KC.N,    KC.M, KC.COMM,  KC.DOT,  KC.SLSH, KC.RSFT,\
        KC.LGUI,   KC.LCTL, LOWER,   KC.SPC,  KC.X,    KC.X,                KC.LGUI, KC.B,    KC.B,    KC.X,  KC.X,    KC.X,
    ],
    [ # LOWER
        KC.TAB,    KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,               KC.N6,   KC.N7,   KC.N8,   KC.N9, KC.N0,   KC.BSPC,\
        KC.CLCK,   _______, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                KC.H,    KC.J,    KC.K,    KC.L,  KC.SCLN, KC.QUOT,\
        KC.LSFT,   XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                KC.N,    KC.M, KC.COMM,  KC.DOT,  KC.SLSH, KC.RSFT,\
        KC.LGUI,   KC.LCTL, LOWER,   KC.SPC,  KC.X,    KC.X,                KC.LGUI, KC.B,    KC.B,    KC.X,   KC.X,  KC.X,
    ]

]

encoder_handler.map = (
    ((KC.UP, KC.DOWN),),
)
keyboard.modules.append(encoder_handler)

if __name__ == '__main__':
    keyboard.go()
