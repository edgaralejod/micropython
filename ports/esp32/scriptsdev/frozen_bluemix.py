from mqtt_simple import MQTTClient

class Bluemix(MQTTClient):
    def __init__(self, org, device_id, device_type, token, auth='use-token-auth',
                 topic='iot-2/evt/status/fmt/json', ssl=False):
        self.client_id = 'd:' + org + ':' + device_type + ':' + device_id
        self.host = org + '.messaging.internetofthings.ibmcloud.com'
        self.topic = topic
        if ssl:
            self.port = 8883
        else:
            self.port = 1883
        self.auth = auth
        MQTTClient.__init__(self, self.client_id, self.host,
                            self.port, self.auth, token)
