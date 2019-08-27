import os
import pigpio

class PiRGBLight(object):
	def __init__(self, r_pin=19, g_pin=20, b_pin=21):
		self._pins = (r_pin, g_pin, b_pin)
		self._pi = pigpio.pi()
		self._color = (0,0,0)
		self._update_color(self._color)

	@property
	def color(self):
		return self._color

	def _update_color(self, rgb):
		color = [min(255, max(0, int(i))) for i in rgb]

		for val, pin in zip(color, self._pins):
			self._pi.set_PWM_dutycycle(pin, val)

		return tuple(color)

	@color.setter
	def color(self, rgb):
		self._color = self._update_color(rgb)
