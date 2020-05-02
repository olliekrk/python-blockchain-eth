import paho.mqtt.client as mqtt

class MQTTListener(mqtt.Client):
    def __init__(self, host, port):
        super().__init__()
        
    def on_connect(client, userdata, flags, result_code):
         