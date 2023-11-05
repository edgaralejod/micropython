
from waterbot import Waterbot
import time
import machine
import json


Pin = machine.Pin
ADC = machine.ADC
I2C = machine.I2C

#Method that runs the analog subsystem and gets data out of it
def run_dacquisition(sensorSetting, afeGain, anChann, pgaSetting, freqStart, freqInc, vSetting, sampleSize, topic):
    global waterbot
    data = {}
    data['status'] = 'running'
    data['recSampSize'] = sampleSize
    mqqtdata = json.dumps(data)
    #client.publish(cfg.RUNTOPIC, mqqtdata, qos=0)
    waterbot.setAnalogSwitch( sensorSetting, afeGain, anChann )
    print(sampleSize)
    data['sweepData'] = waterbot.sweepCommand(pgaSetting, freqStart, freqInc, vSetting, sampleSize)
    mqqtdata = data['sweepData']
    mqqtdata = json.dumps(mqqtdata)
    print(mqqtdata)
    #client.publish(topic, mqqtdata)
    waterbot.clearSweepObject()
    
print("Wb Simple Test Version2 2020-04-20")
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
run_dacquisition(72, 2, 16, 1, 3000, 1000, 0, 6, 'iot-2/evt/aninit/fmt/json')