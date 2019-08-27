from flask import Flask, jsonify, request

from .pirgbled import PiRGBLed

def generate_app(name='ColorSwitch', location=None, r_pin=19, g_pin=20, b_pin=21):
	app = Flask(__name__)
	led = PiRGBLed(r_pin, g_pin, b_pin)

	@app.route('/color', methods=['GET', 'POST'])
	def color():
		if request.method == 'GET':
			r,g,b = led.color

			return jsonify({
				"red": r,
				"green": g,
				"blue": b,
			})
		if request.method == 'POST':
			json_in = request.get_json()

			if not json_in:
				return jsonify({'errors': [
					'Could not read body'
				]}), 400

			rgb = (
				json_in.get('red', 0),
				json_in.get('green', 0),
				json_in.get('blue', 0)
			)
			led.color = rgb

			return '', 204

	@app.route('/info', methods=['GET'])
	def info():
		return jsonify({
			'name': name,
			'location': location
		})

	return app
