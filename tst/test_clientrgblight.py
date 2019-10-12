from unittest import TestCase
from unittest.mock import patch

from pirgblight import ClientRGBLight, clientrgblight
from pirgblight._utils import rgb_tuple_to_json, json_to_rgb_tuple

class GetResponse:
    def __init__(self, rgb=(0,0,0,)):
        self._rgb = rgb

    def json(self):
        return rgb_tuple_to_json(self._rgb)

class ClientRGBLightTest(TestCase):
    @patch.object(clientrgblight, 'get')
    @patch.object(clientrgblight, 'post')
    def test_calls_correct_methods(self, post_mock, get_mock):
        led = ClientRGBLight('host', 'port')

        led.color = (1,2,3,)
        post_mock.assert_called_with('http://host:port/color', json=rgb_tuple_to_json((1,2,3,)))

        get_mock.return_value = GetResponse()
        self.assertTupleEqual(led.color, (0,0,0,))
        get_mock.assert_called_with('http://host:port/color')