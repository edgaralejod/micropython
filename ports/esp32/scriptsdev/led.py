
from machine import Pin

RED_LED = Pin(22, Pin.OUT)
BLUE_LED = Pin(23, Pin.OUT)
GREEN_LED = Pin(25, Pin.OUT)
RED_LED.off()
BLUE_LED.off()
GREEN_LED.off()
# These values would be the correct use for PWM.duty(), but right now just serves as a few colors to call
# Can implement PWM at a different time, this isn't a light show
colorsLibrary = {
    'red': {'r': 1023, 'g': 0, 'b': 0, 'state':'off'},
    'orange': {'r': 1023, 'g': 508, 'b': 0, 'state':'off'},
    'yellow': {'r': 1023, 'g': 1023, 'b': 0, 'state':'off'},
    'green': {'r': 0, 'g': 1023, 'b': 0, 'state':'off'},
    'blue': {'r': 0, 'g': 0, 'b': 1023, 'state':'off'},
    'indigo': {'r': 184, 'g': 172, 'b': 380, 'state':'off'},
    'violet': {'r': 556, 'g': 0, 'b': 1023, 'state':'off'},
    'white': {'r': 1023, 'g': 1023, 'b': 1023, 'state':'off'}
}

def led_toogle(color):
    color = colorsLibrary[color]
    if color['state'] == 'off':
        led_rgb(color['r'],color['g'], color['b'] )
        color['state'] = 'on'
    else:
        led_off()
        color['state'] = 'off'

def led_color(color):
    color = colorsLibrary[color]
    color['state'] = 'on'
    led_rgb(color['r'],color['g'], color['b'] )

def led_rgb(r, g, b):
    RED_LED.value(r)
    GREEN_LED.value(g)
    BLUE_LED.value(b)

def led_off():
    RED_LED.off()
    BLUE_LED.off()
    GREEN_LED.off()
    for index in colorsLibrary:
        color = colorsLibrary[index]
        color['state'] = 'off'


