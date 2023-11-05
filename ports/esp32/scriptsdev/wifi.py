# import config
# import network #type: ignore
# import time
from machine import Pin #type: ignore
from waterbot_led import WaterBotLED, LEDColors

red = Pin(22, Pin.OUT)
blue = Pin(23, Pin.OUT)
green = Pin(25, Pin.OUT)

wbt_led = WaterBotLED(red, green, blue)

wbt_led.led_color(LEDColors.RED)

# # Wireless Station
# sta_if = network.WLAN(network.STA_IF)
# ap_if = network.WLAN(network.AP_IF)

# def connectWiFi():
#     if not sta_if.isconnected():
#         print('connecting to network...')
#         sta_if.active(True)
#         sta_if.connect(config.wifi_config['ssid'], config.wifi_config['password'])
#         while not sta_if.isconnected():
#             pass
#     print('network config: {}'.format(sta_if.ifconfig()))
#     led_pin.value(1)
#     time.sleep(1)
#     led_pin.value(0)
#     time.sleep(1)


# # Wireless Access Point
# ap_if = network.WLAN(network.AP_IF)
# ap_if.active(True)
# print('access point: ', ap_if.active())

# # Complete project details at https://RandomNerdTutorials.com

# def accessPointMode():
#     try:
#         import usocket as socket
#     except:
#         import socket

#     import network

#     import esp
#     esp.osdebug(None)

#     import gc
#     gc.collect()

#     ssid = '_WaterBotSetup'
#     password = 'waterbot'

#     ap = network.WLAN(network.AP_IF)
#     ap.active(True)
#     ap.config(essid=ssid,authmode=4,password=password)

#     while ap.active() == False:
#         pass

#     print('Connection successful')
#     print(ap.ifconfig())

#     def web_page():
#         html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
#         <body><h1>Hello, World!</h1></body></html>"""
#         return html

#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind(('', 80))
#     s.listen(5)

#     while True:
#         conn, addr = s.accept()
#         print('Got a connection from %s' % str(addr))
#         request = conn.recv(1024)
#         print('Content = %s' % str(request))
#         response = web_page()
#         conn.send(response)
#         conn.close()

