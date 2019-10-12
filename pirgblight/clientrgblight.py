from requests import get, post

from ._utils import rgb_tuple_to_json, json_to_rgb_tuple
from .rgblight import RGBLight

class ClientRGBLight(RGBLight):
    def __init__(self, host, port, protocol='http'):
        self._url = "{protocol}://{host}:{port}".format(host=host, port=port, protocol=protocol)

    @property
    def color(self):
        r = get(self._url + '/color')
        data = r.json()

        return json_to_rgb_tuple(data)

    @color.setter
    def color(self, rgb):
        post(self._url + '/color', json=rgb_tuple_to_json(rgb))

    @property
    def info(self):
        r = get(self._url + '/info')
        return r.json()