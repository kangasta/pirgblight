# pirgblight server

The server to run on the device controlling the LED.

## Example request

```python
from requests import post

post('http://192.168.1.43:8080/color', json={"red": 128, "green": 128, "blue": 128})
```