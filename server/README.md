# pirgblight server

The server to run on the device controlling the LED.

## Example request

Assuming the server is running in `localhost`s port `8080`, the following code will send requests to fade on and off first all colors simultaneously and then individually.

```python
from math import pi, cos
from requests import post
from time import sleep

T = 1
N = 10

# Helper function to create generator for n + 1 length fade in out sequence
fade_in_out = lambda n: ((1 - cos(i / n * 2 * pi)) / 2.0 * 255 for i in range(n + 1))

for brightness in fade_in_out(N):
	post('http://localhost:8080/color', json={
		"red": brightness,
		"green": brightness,
		"blue": brightness
	})
	sleep(T / float(N))

for component in ('red', 'green', 'blue',):
	for brightness in fade_in_out(N):
		post('http://localhost:8080/color', json={
			component: brightness
		})
		sleep(T / float(N))
```