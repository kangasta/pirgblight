# pirgblight

[![Build Status](https://travis-ci.org/kangasta/pirgblight.svg?branch=master)](https://travis-ci.org/kangasta/pirgblight)

Server and Home Assistant integration for controlling RGB light via remote Raspberry Pi.

![Red, green, and blue LEDs connected to Raspberry Pi Zero](./img/preview.jpg)

## Usage

Start the server on your rasperry pi where RGB LED is connected to GPIO pins with command:

```bash
pirgblight-server

# OR to see possible parameters:
pirgblight-server -h
```

### Example requests for the server

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

### Home assistant configuration for remote control

In order to follow these instruction, `Configurator` and `SSH server` add-ons for Home assistant might be required. First, clone this repository to `/config/custom_components` directory of your home assistant device:

```bash
mkdir -p /config/custom_components
cd /config/custom_components

git clone https://github.com/kangasta/pirgblight.git
```

This will create directory named `pirgblight` with `manifest.json`, `__init__.py`, and `light.py`, which is what is required by Home assistant.

Then, add configuration item for the light in `configuration.yaml`, for example:

```yaml
light:
- platform: pirgblight
  host: "127.0.0.1"
  port: 8080
```

### Follow brightness and color of another light

Home assistant automations to follow state of an another light:

```yaml
- alias: Follow another light
  trigger:
  - event_data:
      entity_id: light.to_follow
    event_type: state_changed
    platform: event
  condition: []
  action:
  - service: light.turn_on
    entity_id: light.follower
    data_template:
      brightness: '{{ trigger.event.data.new_state.attributes.brightness }}'
      hs_color:
      - '{{ trigger.event.data.new_state.attributes.hs_color[0]|float }}'
      - '{{ trigger.event.data.new_state.attributes.hs_color[1]|float }}'
- alias: Auto-OFF
  trigger:
  - entity_id: light.to_follow
    platform: state
    from: 'on'
    to: 'off'
  condition: []
  action:
  - service: light.turn_off
    entity_id: light.follower
```

## Testing

Run static code analysis with command:

```bash
pylint light.py bin/* pirgblight/ tst/
```

Run unit tests with commands:

```bash
python3 -m unittest discover -s tst/
```

Get test coverage with commands:

```bash
coverage run --source ./ --omit setup.py -m unittest discover tst/
coverage report -m
```
