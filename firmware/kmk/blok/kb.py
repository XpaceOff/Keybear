import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation

# TODO: Rotary encoder to work in both sides of the keyboard
# from kmk.scanners.keypad import MatrixScanner
# from kmk.scanners.encoder import RotaryioEncoder

class KMKKeyboard(_KMKKeyboard):
    col_pins = (board.GP29, board.GP28, board.GP27, board.GP26, board.GP22, board.GP20,)
    row_pins = (board.GP04, board.GP05, board.GP06, board.GP07,)
    diode_orientation = DiodeOrientation.COLUMNS
    encoder_pin_a = board.GP08
    encoder_pin_b = board.GP09
    rgb_pixel_pin = board.GP21
    data_pin_rx = board.RX
    data_pin_tx = board.TX

    # flake8: noqa
    # fmt: off
    coord_mapping = [
     0,  1,  2,  3,  4,  5,  29, 28, 27, 26, 25, 24,
     6,  7,  8,  9, 10, 11,  35, 34, 33, 32, 31, 30,
    12, 13, 14, 15, 16, 17,  41, 40, 39, 38, 37, 36,
        18, 19, 20, 21, 22,  46, 45, 44, 43, 42
    ]
