import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_HS_COLOR,
    PLATFORM_SCHEMA,
    SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR,
    Light
)

from homeassistant.const import CONF_HOST, CONF_PORT

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PORT, default='8080'): cv.port
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    host = config[CONF_HOST]
    port = config[CONF_PORT]

    add_entities(PiRgbLight(host, port))

from requests import get, post
from colorsys import hls_to_rgb, rgb_to_hls

class PiRgbLight(Light):
    def __init__(self, host, port):
        self._url = "http://{host}:{port}".format(host=host, port=port)
        self._h = 0
        self._s = 0
        self._l = 0
        self._name = None

    @property
    def name(self):
        return self._name

    @property
    def supported_features(self):
        return SUPPORT_COLOR | SUPPORT_BRIGHTNESS

    @property
    def is_on(self):
        return self._l > 0

    @property
    def brightness(self):
        return self._l * 255

    @property
    def hs_color(self):
        return [self._h * 360, self._s * 100]

    def turn_on(self, **kwargs):
        l = kwargs.get(ATTR_BRIGHTNESS, 0) 
        h, s = kwargs.get(ATTR_HS_COLOR, [0.0,0.0])
        self._h, self._s, self._l = [h / 360.0, s / 100.0, l / 255.0]

        r,g,b = hls_to_rgb(self._h, self._l, self._s)
        post(self._url + '/color', data={
            'red': r * 255.0,
            'green': g * 255.0,
            'blue': b * 255.0
        })

    def turn_off(self, **kwargs):
        self._l = 0

    def update(self):
        r = get(self._url + '/info')
        self._name = r.json()['name']

        r = get(self._url + '/color')
        data = r.json()

        rgb = (
            data.get('red', 0) / 255.0,
            data.get('green', 0) / 255.0,
            data.get('blue', 0) / 255.0,
        )

        self._h, self._l, self._s = rgb_to_hls(*rgb)
