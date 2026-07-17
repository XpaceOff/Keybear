import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.quickpin.pro_micro.nice_nano import pinout as pins
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    # -----------------------------------------------------------------------
    # Matrix — same physical PCB as the BLOK version, mapped via Pro Micro
    # pinout indices so the same board works with nice!nano v2.
    #
    # Index reference (nice_nano quickpin):
    #   idx  6 = P0_22   idx  7 = P0_24   idx  8 = P1_00   idx  9 = P0_11
    #   idx 14 = P1_11   idx 15 = P1_13   idx 16 = P1_15   idx 17 = P0_02
    #   idx 18 = P0_29   idx 19 = P0_31
    # -----------------------------------------------------------------------
    col_pins = (pins[19], pins[18], pins[17], pins[16], pins[15], pins[14],)
    row_pins = (pins[6],  pins[7],  pins[8],  pins[9],)
    diode_orientation = DiodeOrientation.COLUMNS

    # Rotary encoder
    encoder_pin_a = pins[10]   # P1_04
    encoder_pin_b = pins[11]   # P1_06

    # RGB underglow / per-key
    rgb_pixel_pin = pins[12]   # P0_09

    # Wired UART split (TRRS cable)  — hardware UART pins, no PIO needed
    data_pin    = board.RX     # pins[1]
    data_pin_tx = board.TX     # pins[0]

    # fmt: off
    coord_mapping = [
     0,  1,  2,  3,  4,  5,  29, 28, 27, 26, 25, 24,
     6,  7,  8,  9, 10, 11,  35, 34, 33, 32, 31, 30,
    12, 13, 14, 15, 16, 17,  41, 40, 39, 38, 37, 36,
        18, 19, 20, 21, 22,  46, 45, 44, 43, 42
    ]
    # fmt: on
