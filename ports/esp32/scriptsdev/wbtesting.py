import machine  # type: ignore
from waterbot import Waterbot
import time
import network  # type: ignore
import gc
from local_websocket import LocalWebSocketProcess

gc.collect()


Pin = machine.Pin
SDCard = machine.SDCard
ADC = machine.ADC
I2C = machine.I2C

ssid = "ATTJ6nak8s"
password = "ghr8#34zjt6y"


last_message = 0
message_interval = 5
counter = 0
print("Wb Socket test")
i2c = I2C(0, scl=Pin(18), sda=Pin(19), freq=40000)
sd = SDCard(slot=1, width=4, freq=20000000)

red = Pin(22, Pin.OUT)
blue = Pin(23, Pin.OUT)
green = Pin(25, Pin.OUT)
an_sns_en = Pin(26, Pin.OUT)
an_sns = ADC(Pin(34))
analog_enable = Pin(27, Pin.OUT)
red.off()
blue.off()
green.off()

green.on()
red.on()
time.sleep(1)
green.off()
red.off()
analog_enable.on()
waterbot = Waterbot(i2c, red, green, blue)
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass

print("Connection successful")
print(station.ifconfig())
# ssid = 'MicroPython-AP'
# password = 'WbtDemo1990'

# ap = network.WLAN(network.AP_IF)
# ap.active(True)
# ap.config(essid=ssid, password=password, authmode=network.AUTH_WPA_WPA2_PSK)

# while ap.active() == False:
#   pass

# print('Connection successful')
# print(ap.ifconfig())

wb = LocalWebSocketProcess(waterbot)
wb.socketConnect()
