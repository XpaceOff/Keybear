print("Starting")

from kb import KMKKeyboard
from kmk.keys import KC

from kmk.modules.split import Split, SplitSide, SplitType

keyboard = KMKKeyboard()

split = Split(split_flip=False, split_side=SplitSide.RIGHT,split_target_left=False)
keyboard.modules.append(split)

keyboard.keymap = [
    [
        KC.TAB,    KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,                         KC.Y,    KC.U,    KC.I,    KC.O,   KC.P,  KC.BSPC,\
        KC.LCTL,   KC.A,    KC.S,    KC.D,    KC.F,    KC.G,                         KC.H,    KC.J,    KC.K,    KC.L, KC.SCLN, KC.QUOT,\
        KC.LSFT,   KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,                         KC.N,    KC.M, KC.COMM,  KC.DOT, KC.SLSH, KC.RSFT,\
                                            KC.LGUI,   KC.B,  KC.B,     KC.ENT,   KC.N,  KC.RALT,
    ]
]

if __name__ == '__main__':
    keyboard.go()