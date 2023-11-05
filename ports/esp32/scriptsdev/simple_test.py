import machine
from waterbot import Waterbot

import os
import time
import ubinascii
import micropython
import network
import json



Pin = machine.Pin
ADC = machine.ADC
I2C = machine.I2C

print("Wb Simple Test")
i2c = I2C(0, scl=Pin(18), sda=Pin(19), freq=40000)

red = Pin(22, Pin.OUT)
blue = Pin(23, Pin.OUT)
green = Pin(25, Pin.OUT)
an_sns_en = Pin(26, Pin.OUT)
analog_enable = Pin(27, Pin.OUT)
an_sns = ADC(Pin(34))

red.off()
blue.off()
green.off()

green.on()
red.on()
time.sleep(1)
green.off()
red.off()
analog_enable.on()
waterbot = Waterbot(i2c)
waterbot.ad5934Init()
data = waterbot.sweepCommand(1, 4000, 100, 0, 1)
print(data)
#help(waterbot)