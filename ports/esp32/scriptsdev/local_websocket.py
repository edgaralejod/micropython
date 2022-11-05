from uwebsocket import websocket
import websocket_helper
import socket as usock
import network 
import time
import json
import _thread
import gc

class LocalWebSocketProcess:
    def __init__(self, waterbot, port=8266):
        self._socket = None
        self._port = port   
        self._ws = None
        self._runTest = False
        self._waterbot = waterbot
        waterbot.ad5934Init()
        self._emptypktcnt = 0
        self._threadRunning = False
        f = open('syscal.txt')
        eval_syscal = eval(f.read())
        f.close()
        self._syscal_port1 = eval_syscal[0]
        self._syscal_port2 = eval_syscal[1]

    def socketConnect(self):    
        self._socket = usock.socket()
        self._socket.setsockopt(usock.SOL_SOCKET, usock.SO_REUSEADDR, 1)
        ai = usock.getaddrinfo("0.0.0.0", self._port)
        addr = ai[0][4]
        self._socket.bind(addr)
        self._socket.listen(1)
        self._socket.setsockopt(usock.SOL_SOCKET, 20, self.socketAcceptHandler)
        for i in (network.AP_IF, network.STA_IF):
            iface = network.WLAN(i)
            if iface.active():
                print("Websocket started on ws://%s:%d" % (iface.ifconfig()[0], self._port))       

    def socketAcceptHandler(self, socket):
        if self._ws is None:
            cl, remote_addr = socket.accept()
            print("WebSocket connection from:", remote_addr)
            websocket_helper.server_handshake(cl)
            self._ws = websocket(cl, True)
            cl.setblocking(False)
            cl.setsockopt(usock.SOL_SOCKET, 20, self.socketCallback)
            self._socket = cl
            _thread.start_new_thread(self.startTest, ())
        else:
            print("No concurrent connections supported")
            self.closeSocket()

    def socketCallback(self, socket):
        try:
            data = str(self._ws.read(), 'utf-8')
            print('In Socket Callback ws:' + data)
            if len(data) > 0:
                if 'startDemo' in data:
                    self._runTest = True
                    print(gc.mem_free())
                    self._threadRunning = True
                if 'stopDemo' in data:
                    self._runTest = False
                    gc.collect()
            else:
                
                self._emptypktcnt = self._emptypktcnt + 1
                if ( self._emptypktcnt >= 5 ):
                    self.closeSocket()

        except Exception as e:
            print('Exception:', e)
            print("Closing connection.")
            self.closeSocket()

    def startTest(self):
        print('Start Test')
        try:
            while True:
                if self._runTest:
                    if self._ws is None:
                        print('WebSocket is closed')
                        self._runTest = False
                    else:
                        self._waterbot.clearSweepObject()
                        self._waterbot.setAnalogSwitch (
                            self._waterbot.ADG715_1, 
                            self._waterbot.ADG715_YX, 
                            self._waterbot.ADG715_RFBK_1K
                        )                
                        data = self._waterbot.sweepCommand(1, 4000, 100, 0, 1)
                        #print(data)
                        local_mag = data[0]['magnitude']
                        #print(local_mag)
                        sys_gain = self._syscal_port2[0]['data'][1]['gainFactor']
                        #print(sys_gain)
                        local_sysmag = (1)/((local_mag)*(sys_gain))
                        cond1 = ((1)/(local_sysmag))*0.65
                        cond1 = cond1*pow(10,6)
                        self._waterbot.clearSweepObject()
                        self._waterbot.setAnalogSwitch (
                            self._waterbot.ADG715_2, 
                            self._waterbot.ADG715_YX, 
                            self._waterbot.ADG715_RFBK_1K
                        )
                        data = self._waterbot.sweepCommand(1, 4000, 100, 0, 1)
                        #print(data)
                        local_mag = data[0]['magnitude']
                        #print(local_mag)
                        sys_gain = self._syscal_port2[1]['data'][1]['gainFactor']
                        #print(sys_gain)
                        local_sysmag = (1)/((local_mag)*(sys_gain))
                        cond2 = ((1)/(local_sysmag))*0.65
                        cond2 = cond2*pow(10,6)
                        data = {
                            'cond1': cond1,
                            'cond2': cond2
                        }
                        self._ws.write(json.dumps(data))
                        time.sleep(0.1)
        except Exception as e:
            print('Exception in thread: ' + str(e))

    
    def closeSocket(self):
        if self._socket is None:
            print('Already Closed')
        else:
            self._runTest = False
            self._socket.setsockopt(usock.SOL_SOCKET, 20, None)
            self._socket.close()
            self._socket = None
            self._ws = None        
            self._emptypktcnt = 0