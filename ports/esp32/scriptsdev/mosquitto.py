#main.py -- put your code here!
import network
import machine
import mqtt_simple
import time
import ujson as json
import waterbot as wb
import config as cfg
import _thread
from micropython import schedule
#Board Initialization
SPI = machine.SPI(1)
CS = machine.Pin("A4")
RST = machine.Pin("D9")
IRQ = machine.Pin("D10")

#Turn on the analog System.
analog_pwr = machine.Pin("D14", machine.Pin.OUT_PP)
analog_pwr.value(1)

#Globals
client = None
waterbot = None
keepalive_time = 10

#Method that receives and parses information from the broker
def rec_callback(topic, msg):
    global client
    topic = str(topic, "utf-8") 
    msg = str(msg, "utf-8")
    print(topic)
    print(msg)
    try:
      if ( ("syscal" in topic) or 
           ("condrd" in topic) or
           ("condcal" in topic) or
           ("sweep" in topic) ):
        msg_json = json.loads(msg)
        sset = int(msg_json['portsetting'])
        again = int(msg_json['afegain'])
        anChann = int(msg_json['switchsetting'])
        pgas = int(msg_json['intpga'])
        freqs = int(msg_json['startfreq'])
        freqi = int(msg_json['freqinc'])
        vset = int(msg_json['pkpkvolt'])
        samps = int(msg_json['numbersamples'])
        if "syscal" in topic:
          run_dacquisition(sset, again, anChann, pgas, freqs, freqi, vset, samps, cfg.SYSCALTOPIC)  
        elif "condrd" in topic:
          run_dacquisition(sset, again, anChann, pgas, freqs, freqi, vset, samps, cfg.CONDRDTOPIC)
        elif "condcal" in topic:
          run_dacquisition(sset, again, anChann, pgas, freqs, freqi, vset, samps, cfg.CONDCALTOPIC) 
        elif "sweep" in topic:
          run_dacquisition(sset, again, anChann, pgas, freqs, freqi, vset, samps, cfg.SWEEPTOPIC)     

      elif "ping" in topic:
        print("Ping Received")
        data = {}
        data['job_time'] = msg
        mqqtdata = json.dumps(data)
        client.publish(cfg.PINGTOPIC, mqqtdata, qos=0)

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
        client.disconnect()
        machine.reset()

      else :  
        print("anotherCommand")

    except Exception as e:
      print("Command Received Exception: " + str(e))

def ping_thread():
    global client
    global keepalive_time
    while True:
        time.sleep(keepalive_time)
        client.ping()
        print('Sent Mqtt Ping')  
        
#Method that runs the analog subsystem and gets data out of it
def run_dacquisition(sensorSetting, afeGain, anChann, pgaSetting, freqStart, freqInc, vSetting, sampleSize, topic):
    global client
    global waterbot
    data = {}
    data['status'] = 'running'
    data['recSampSize'] = sampleSize
    mqqtdata = json.dumps(data)
    client.publish(cfg.RUNTOPIC, mqqtdata, qos=0)
    waterbot.setAnalogSwitch( sensorSetting, afeGain, anChann )
    data['sweepData'] = waterbot.sweepCommand(pgaSetting, freqStart, freqInc, vSetting, sampleSize)
    mqqtdata = data['sweepData']
    mqqtdata = json.dumps(mqqtdata)
    client.publish(topic, mqqtdata)
    waterbot.clearSweepObject()


print("Starting main...")
nic = network.RS9113(SPI, CS, RST, IRQ)
print("WiFi Initialized")
ret_obj = {}
ret_obj['networks'] = nic.scan()
print('Networks: {}'.format(ret_obj))
ssid = 'NETGEAR97'
psk = 'purpletrail985'
if nic.connect(ssid, key=psk, ssl=False, nonblocking=True) is False:
    raise ConnectError("Can't connect to {}".format(ssid))
else:
    print("WiFi connected to {}".format(ssid))
    print(nic.ifconfig())

client = mqtt_simple.MQTTClient(client_id='E238000148', server='192.168.0.58', port=1883, user='E238000148', password='ThisIsThePassword', keepalive=0)
client.connect()
client.set_callback(rec_callback)
client.subscribe(cfg.SUBSCRIBE)

waterbot = wb.waterbot()
waterbot.ad5934Init()
run_dacquisition(72, 2, 16, 1, 3000, 100, 0, 2, cfg.ANINIT)
#_thread.start_new_thread(ping_thread, ())
timeout_cnt = 0
while True:
    resp = client.check_msg()
    if resp is None:
        #time.sleep(0.1)
        timeout_cnt = timeout_cnt + 1
    else:
        print('The scheduled data: {}'.format(resp))
        print('The timeout cnt: {}'.format(timeout_cnt))
        timeout_cnt = 0
