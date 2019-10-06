from unittest import TestCase
from unittest.mock import MagicMock, patch

from pirgblight import RGBLight

class RgbLightTest(TestCase):
    def test_raises_not_implemented_error(self):
        led = RGBLight()

        with self.assertRaises(NotImplementedError):
            led.color

        with self.assertRaises(NotImplementedError):
            led.color = (4, 5, 6,)
