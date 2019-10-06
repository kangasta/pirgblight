from requests import get, post

from .rgblight import RGBLight

class ClientRGBLight(RGBLight):
    def __init__(self, host, port, protocol='http'):
        self._url = "{protocol}://{host}:{port}".format(host=host, port=port, protocol=protocol)

    @property
    def color(self):
        r = get(self._url + '/color')
        data = r.json()

        return (
            data.get('red', 0),
            data.get('green', 0),
            data.get('blue', 0),
        )

    @color.setter
    def color(self, rgb):
        r, g, b = rgb

        post(self._url + '/color', json={
            'red': r,
            'green': g,
            'blue': b,
        })

    @property
    def info(self):
        r = get(self._url + '/info')
        return r.json()