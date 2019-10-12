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

from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PORT, default=8080): cv.port,
    vol.Optional(CONF_NAME): cv.string,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)
    name = config.get(CONF_NAME)

    add_entities([PiRgbLight(host, port, name)])

from .pirgblight import ClientRGBLight

class PiRgbLight(Light):
    def __init__(self, host, port, name=None):
        self._client = ClientRGBLight(host, port)
        self._h = 0
        self._s = 0
        self._v = 0
        self._on = False
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def supported_features(self):
        return SUPPORT_COLOR | SUPPORT_BRIGHTNESS

    @property
    def is_on(self):
        return self._on

    @property
    def brightness(self):
        return self._v * 255

    @property
    def hs_color(self):
        return [self._h * 360, self._s * 100]

    def turn_on(self, **kwargs):
        self._on = True

        v = kwargs.get(ATTR_BRIGHTNESS, self._v * 255)
        h, s = kwargs.get(ATTR_HS_COLOR, [self._h * 360, self._s * 100])

        self._h, self._s, self._v = [h / 360.0, s / 100.0, v / 255.0]

        self._client.hsv_color = (self._h, self._s, self._v,)

    def turn_off(self, **kwargs):
        self._on = False
        self._client.hsv_color = (0, 0, 0,)

    def update(self):
        if not self._name:
            self._name = self._client.info['name']

        self._h, self._s, self._v = self._client.hsv_color
