from flask import Flask, jsonify, request

from pirgbled import PiRGBLed

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

if __name__ == '__main__':
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument("--pins",
		help="Pin numbers for R, G, and B",
		default=(19, 20, 21,),
		type=int,
		nargs=3,
		metavar=("R","G","B"))
	parser.add_argument("--name",
		help="name of the light",
		default="pirgblight",
		type=str)
	parser.add_argument("--location",
		help="location of the light",
		default=None,
		type=str)
	parser.add_argument("--host",
		help="hosts to serve to (default = 0.0.0.0)",
		default="0.0.0.0",
		type=str)
	parser.add_argument("-p","--port",
		help="port to serve from (default = 8080)",
		default=8080,
		type=int)

	args = parser.parse_args()

	generate_app(args.name, args.location, *args.pins).run(use_reloader=True, host=args.host, port=args.port, threaded=True)
