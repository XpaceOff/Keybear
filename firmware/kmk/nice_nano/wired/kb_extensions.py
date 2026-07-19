import gc
from kmk.modules.layers import Layers as _Layers
from kmk.extensions.lock_status import LockStatus
from kmk.modules.cg_swap import CgSwap as _CgSwap
from kmk.extensions import Extension

import digitalio
import adafruit_pixelbuf
from neopixel_write import neopixel_write

class Layers(_Layers):
    """Update the Layer key LED colour when the active layer changes.
    In the LOWER layer, pressing a-z or ENTER returns to DEFAULT."""

    first_boot     = True
    last_top_layer = 0
    hues = (10, 20, 69, 100, 180, 250, 35)

    def __init__(self, rgb, led_index):
        super().__init__()
        self._rgb = rgb
        self._led = led_index

    def after_hid_send(self, keyboard):
        if keyboard.active_layers[0] == 1:
            for nkey in keyboard.keys_pressed:
                if nkey.code >= 4 and nkey.code <= 29 or nkey.code == 40:
                    self._active_combo = None
                    keyboard.active_layers.clear()
                    keyboard.active_layers.insert(0, 0)
                    break

        if keyboard.active_layers[0] != self.last_top_layer or self.first_boot:
            self.first_boot     = False
            self.last_top_layer = keyboard.active_layers[0]
            self._rgb.set_hsv(
                self.hues[self.last_top_layer], 255, self._rgb.val, self._led,
            )
            self._rgb.show()

class LEDLockStatus(LockStatus):
    """Light the Caps Lock LED when active."""

    first_boot = True

    def __init__(self, rgb, led_index):
        super().__init__()
        self._rgb = rgb
        self._led = led_index

    def set_lock_leds(self):
        if self.get_caps_lock():
            self._rgb.set_hsv(100, 255, self._rgb.val, self._led)
        else:
            self._rgb.set_hsv(0, 0, 0, self._led)
        self._rgb.show()

    def after_hid_send(self, sandbox):
        if self.first_boot:
            self.set_lock_leds()
            self.first_boot = False
        super().after_hid_send(sandbox)
        if self.report_updated:
            self.set_lock_leds()

class CgSwap(_CgSwap):
    """Update the GUI key LED when CG-swap state changes."""

    last_swap_state = False
    first_boot      = True

    def __init__(self, rgb, led_index, hue_values):
        super().__init__()
        self._rgb  = rgb
        self._led  = led_index
        self._hues = hue_values          # [win/linux, mac]

    def after_hid_send(self, keyboard):
        if self.last_swap_state != self.cg_swap_enable or self.first_boot:
            self.last_swap_state = self.cg_swap_enable
            self.first_boot      = False
            this_hue = self._hues[1] if self.cg_swap_enable else self._hues[0]
            self._rgb.set_hsv(this_hue, 255, self._rgb.val, self._led)
            self._rgb.show()

class GCCollect(Extension):
    def during_bootup(self, keyboard):
        gc.collect()
    def before_matrix_scan(self, keyboard):
        pass
    def after_matrix_scan(self, keyboard):
        pass
    def before_hid_send(self, keyboard):
        pass
    def after_hid_send(self, keyboard):
        pass
    def on_powersave_enable(self, keyboard):
        pass
    def on_powersave_disable(self, keyboard):
        pass

