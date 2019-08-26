# pirgblight

Server and Home Assistant integration for controlling RGB light via remote Raspberry Pi.

## Usage

Start the server on your rasperry pi where RGB LED is connected to GPIO pins with command:

```bash
python3 server/app.py

# OR to see possible parameters:
python3 server/app.py -h
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
