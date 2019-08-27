from unittest import TestCase
from unittest.mock import MagicMock, patch

import pigpio
from pirgblight import generate_app

def to_color_body(r, g, b):
    return {
        'red': r,
        'green': g,
        'blue': b,
    }

class GenerateAppTest(TestCase):
    @patch.object(pigpio, 'pi')
    def test_get_info_provides_server_info(self, _):
        client = generate_app('Test name', 'Test location').test_client()
        info = client.get('/info').json

        self.assertDictEqual({
            'name': 'Test name',
            'location': 'Test location',
        }, info)

    @patch.object(pigpio, 'pi')
    def test_post_color_with_no_body_fails(self, _):
        client = generate_app('Test name').test_client()

        color_res = client.post('/color')

        self.assertEqual(color_res.status_code, 400)

    @patch.object(pigpio, 'pi')
    def test_post_color_triggers_pwm_change(self, mock):
        pi = MagicMock()
        mock.return_value = pi

        pins = (1, 2, 3,)
        rgb = (4, 5, 6,)

        client = generate_app('Test name', 'Test location', *pins).test_client()
        color_status = client.post('/color', json=to_color_body(*rgb)).status_code

        pi.set_PWM_dutycycle.has_calls(call(*z) for z in zip(pins, rgb))
        self.assertEqual(color_status, 204)

    @patch.object(pigpio, 'pi')
    def test_get_color_provides_current_rgb_state(self, _):
        client = generate_app('Test name').test_client()

        color = client.get('/color').json

        self.assertDictEqual(to_color_body(0, 0, 0), color)
