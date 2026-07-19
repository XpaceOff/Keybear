"""Minimal NeoPixel — uses only modules frozen into the nice!nano firmware."""

import digitalio
import adafruit_pixelbuf
from neopixel_write import neopixel_write

GRB = "GRB"
GRBW = "GRBW"
RGBW = "RGBW"

class NeoPixel(adafruit_pixelbuf.PixelBuf):
    def __init__(self, pin, n, *, bpp=3, brightness=1.0, auto_write=True, pixel_order=None):
        if not pixel_order:
            pixel_order = GRB if bpp == 3 else GRBW
        elif isinstance(pixel_order, tuple):
            pixel_order = "".join(RGBW[i] for i in pixel_order)
        self._pin = digitalio.DigitalInOut(pin)
        self._pin.direction = digitalio.Direction.OUTPUT
        super().__init__(n, byteorder=pixel_order, brightness=brightness, auto_write=auto_write)

    def deinit(self):
        self._pin.deinit()

    def _transmit(self, buffer):
        neopixel_write(self._pin, buffer)
