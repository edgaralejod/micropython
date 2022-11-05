import machine
from waterbot import Waterbot
import os
import time
import mqtt_simple
import ubinascii
import micropython
import network
import json
import frozen_config as cfg
import gc
import led
import _thread
gc.collect()
a_lock = None
keepalive_time = 100
Pin = machine.Pin
SDCard = machine.SDCard
ADC = machine.ADC
I2C = machine.I2C
ssid = 'NETGEAR97'
password = 'purpletrail985'
mqtt_server = 'REPLACE_WITH_YOUR_MQTT_BROKER_IP'
bmx_token = 't*PAW)S3VMAx3O_Ug&'
bmx_org = 'um5874'
bmx_devid = 'E300000000'
bmx_devtype = 'Waterbot_ESP32'


last_message = 0
message_interval = 5
counter = 0
print("Hello Hwapi with thread, and lock")
i2c = I2C(0, scl=Pin(18), sda=Pin(19), freq=40000)
sd = SDCard(slot=1, width=4, freq=20000000)

led.led_off()
an_sns_en = Pin(26, Pin.OUT)
an_sns = ADC(Pin(34))
led.led_color('yellow')
waterbot = Waterbot(i2c)

client = None

def ping_thread():
    global client
    global keepalive_time
    global a_lock
    while True:
        time.sleep(keepalive_time/2)
        with a_lock:
          client.ping()
          #print('Sent Mqtt Ping')  

#Method that runs the analog subsystem and gets data out of it
def run_dacquisition(sensorSetting, afeGain, anChann, pgaSetting, freqStart, freqInc, vSetting, sampleSize, topic):
    global client
    global waterbot
    global wdt
    data = {}
    data['status'] = 'running'
    data['recSampSize'] = sampleSize
    mqqtdata = json.dumps(data)
    client.publish(cfg.RUNTOPIC, mqqtdata, qos=0)
    waterbot.setAnalogSwitch( sensorSetting, afeGain, anChann )
    print(sampleSize)
    data['sweepData'] = waterbot.sweepCommand(pgaSetting, freqStart, freqInc, vSetting, sampleSize)
    mqqtdata = data['sweepData']
    mqqtdata = json.dumps(mqqtdata)
    client.publish(topic, mqqtdata)
    waterbot.clearSweepObject()

#Callback that receives the message from the cloud.
def rec_callback(topic, msg):
    global client
    global a_lock

    topic = str(topic, "utf-8") 
    msg = str(msg, "utf-8")
    print(topic)
    return_topic = None
    sweep_req = "sweep" in topic
    syscal_req = "syscal" in topic
    condrd_req = "condrd" in topic
    condcal_req = "condcal" in topic
    if sweep_req :
      return_topic = cfg.SWEEPTOPIC
    elif syscal_req:
      return_topic = cfg.SYSCALTOPIC
    elif condrd_req:
      return_topic = cfg.CONDRDTOPIC
    elif condcal_req:
      return_topic = cfg.CONDCALTOPIC
    print(sweep_req)
    print(msg)
    try:
      if ( sweep_req or syscal_req or condrd_req or condcal_req ) :
        msg_json = json.loads(msg)
        sset = int(msg_json['portsetting'])
        again = int(msg_json['afegain'])
        anChann = int(msg_json['switchsetting'])
        pgas = int(msg_json['intpga'])
        freqs = int(msg_json['startfreq'])
        freqi = int(msg_json['freqinc'])
        vset = int(msg_json['pkpkvolt'])
        samps = int(msg_json['numbersamples'])
        print("Inside data acquisition related topic")
        run_dacquisition(sset, again, anChann, pgas, freqs, freqi, vset, samps, return_topic)  

      elif "ping" in topic:
        print("Ping Received")
        data = {}
        data['job_time'] = msg
        mqqtdata = json.dumps(data)
        with a_lock:
          client.publish(cfg.PINGTOPIC, mqqtdata, qos=0)

      elif "battrd" in topic:
        print("Battery Mode")
        data = {}
        an_sns_en.on()
        data['battlvl'] = an_sns.read()
        an_sns_en.off()
        data['job_time'] = msg
        mqqtdata = json.dumps(data)
        with a_lock:
          client.publish(cfg.BATLTOPIC, mqqtdata, qos=0)

      elif "setswitch" in topic:
        msg_json = json.loads(msg)
        sset = int(msg_json['portsetting'])
        again = int(msg_json['afegain'])
        anChann = int(msg_json['switchsetting'])
        waterbot.setAnalogSwitch( sset, again, anChann )

      elif "clearswitch" in topic:
        print('clear all')
        waterbot.ADG715ClearChannel(waterbot.ADG715_1)
        waterbot.ADG715ClearChannel(waterbot.ADG715_2)

      elif "reset" in topic:
        with a_lock:
          client.disconnect()
        machine.reset()

      else :  
        print("anotherCommand")

    except Exception as e:
      print("Command Received Exception: " + str(e))

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())
a_lock = _thread.allocate_lock()
client = mqtt_simple.MQTTClient(client_id='E238000148', server='192.168.1.109', port=1883, user='E238000148', password='ThisIsThePassword', keepalive=keepalive_time*2)
client.connect()
client.set_callback(rec_callback)
client.subscribe(cfg.SUBSCRIBE)
waterbot.ad5934Init()
run_dacquisition(72, 2, 16, 1, 3000, 100, 0, 2, cfg.ANINIT)
_thread.start_new_thread(ping_thread, ())
timeout_cnt = 0
led.led_color('green')
while True:
    try:
      with a_lock:
        resp = client.check_msg()
        if resp is None:
            #time.sleep(0.1)
            timeout_cnt = timeout_cnt + 1
            if timeout_cnt >= timeout_cnt*100:
              print('timeout exceed 10000, reset?')
              timeout_cnt = 0
        else:
            print('The scheduled data: {}'.format(resp))
            print('The timeout cnt: {}'.format(timeout_cnt))
            timeout_cnt = 0
    except Exception as e:
      print('Exception raised: {}'.format(e))