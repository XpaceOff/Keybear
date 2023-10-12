from kb import KMKKeyboard

from kmk.keys import KC
from kmk.modules.split import Split, SplitSide, SplitType
from kmk.extensions.RGB import RGB

keyboard = KMKKeyboard()

# Adding extensions
rgb = RGB(pixel_pin=keyboard.rgb_pixel_pin, num_pixels=18, hue_default=190)

# TODO Comment one of these on each side
split_side = SplitSide.LEFT
#split_side = SplitSide.RIGHT
split = Split(split_type=SplitType.BLE, split_side=split_side)

keyboard.modules.append(split)
keyboard.extensions.append(rgb)

keyboard.keymap = [
    [
        KC.TAB,    KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,                    KC.Y,    KC.U,    KC.I,    KC.O,   KC.P,  KC.BSPC,\
        KC.CLCK,   KC.A,    KC.S,    KC.D,    KC.F,    KC.G,                    KC.H,    KC.J,    KC.K,    KC.L, KC.SCLN, KC.QUOT,\
        KC.LSFT,   KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,                    KC.N,    KC.M, KC.COMM,  KC.DOT, KC.SLSH, KC.RSFT,\
        KC.LGUI,   KC.LCTL, KC.B,    KC.SPC,  KC.X,    KC.RGB_MODE_KNIGHT,      KC.LGUI, KC.B,    KC.B,    KC.X,   KC.X,  KC.X,
    ]
]

if __name__ == '__main__':
    keyboard.go()
