import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation

class KMKKeyboard(_KMKKeyboard):
    col_pins = (board.GP29, board.GP28, board.GP27, board.GP26, board.GP22, board.GP20,)
    row_pins = (board.GP05, board.GP06, board.GP07, board.GP08,)
    diode_orientation = DiodeOrientation.COLUMNS
    encoder_pin_a = board.GP23 
    encoder_pin_b = board.GP21
    rgb_pixel_pin = board.TX
    data_pin = board.RX

    # flake8: noqa
    # fmt: off
    coord_mapping = [
     0,  1,  2,  3,  4,  5,  29, 28, 27, 26, 25, 24,
     6,  7,  8,  9, 10, 11,  35, 34, 33, 32, 31, 30,
    12, 13, 14, 15, 16, 17,  41, 40, 39, 38, 37, 36,
    18, 19, 20, 21, 22, 23,  47, 46, 45, 44, 43, 42,
    ]
