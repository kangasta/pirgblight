from unittest import TestCase
from unittest.mock import MagicMock, patch

from pirgblight import RGBLight

class DummyRGBLight(RGBLight):
    def __init__(self):
        self._rgb = (0,0,0,)

    @property
    def color(self):
        return self._rgb

    @color.setter
    def color(self, rgb):
        self._rgb = rgb

class RgbLightTest(TestCase):
    def test_raises_not_implemented_error(self):
        led = RGBLight()

        with self.assertRaises(NotImplementedError):
            led.color

        with self.assertRaises(NotImplementedError):
            led.color = (4, 5, 6,)

    def test_supports_hsv_values(self):
        led = DummyRGBLight()
        black = (0,0,0,)
        white = (255,255,255,)

        led.color = black
        self.assertTupleEqual(led.hsv_color, black)

        led.hsv_color = (0,0,1)
        self.assertTupleEqual(led.color, white)
