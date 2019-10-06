from unittest import TestCase
from unittest.mock import MagicMock, patch

import pigpio
from pirgblight import PiRGBLight

class PiRgbLightTest(TestCase):
    @patch.object(pigpio, 'pi')
    def test_allows_custom_pins(self, mock):
        pi = MagicMock()
        mock.return_value = pi

        pins = (1, 2, 3,)
        rgb = (4, 5, 6,)

        led = PiRGBLight(*pins)
        led.color = rgb

        pi.set_PWM_dutycycle.has_calls(call(*z) for z in zip(pins, rgb))
        self.assertEqual(rgb, led.color)
