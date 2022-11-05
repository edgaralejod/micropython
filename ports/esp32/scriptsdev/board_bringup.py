
import led
import time
from machine import *
import os

ssid = "NETGEAR97"
password = "purpletrail985"

print("Board Bring Up program")

led.led_off()

print("Trying green")
led.led_color("green")
time.sleep(1)
print("Trying blue")
led.led_color("blue")
time.sleep(1)
print("Trying Red")
led.led_color("red")
sd = SDCard(slot=1, width=4, freq=500000)
time.sleep(1)
os.mount(sd, "sd2/")
time.sleep(1)
print(os.listdir("d2/"))
i2c = I2C(0, scl=Pin(18), sda=Pin(19), freq=400000)
i2c.scan()