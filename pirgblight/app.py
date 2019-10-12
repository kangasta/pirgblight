from flask import Flask, jsonify, request

from ._utils import rgb_tuple_to_json, json_to_rgb_tuple
from .pirgblight import PiRGBLight

def generate_app(name='ColorSwitch', location=None, r_pin=19, g_pin=20, b_pin=21):
    app = Flask(__name__)
    led = PiRGBLight(r_pin, g_pin, b_pin)

    @app.route('/color', methods=['GET', 'POST'])
    def color():
        if request.method == 'GET':
            return jsonify(rgb_tuple_to_json(led.color))
        if request.method == 'POST':
            json_in = request.get_json()

            if not json_in:
                return jsonify({'errors': [
                    'Could not read body'
                ]}), 400

            led.color = json_to_rgb_tuple(json_in)

            return '', 204

    @app.route('/info', methods=['GET'])
    def info():
        return jsonify({
            'name': name,
            'location': location
        })

    return app
