import sys
import time
import json
import paho.mqtt.client as mqtt
from .mqtt_defaults import *

def _timestamp_now():
    return int(round(time.time())*1000)


class SmartMQTTListener(mqtt.Client):
    def __init__(self, h, host=DEFAULT_HOST, port=DEFAULT_PORT):
        super().__init__(f'SmartListener_{_timestamp_now()}')
        self.connect_async(host, port, KEEPALIVE)
        self.h = h
        
    def listen_on_topic(self, topic, callback, qos=DEFAULT_QOS):
        self.message_callback_add(topic, callback)
        print(f'Subscribing to the [{topic}] topic...')
        self.subscribe(topic, qos)
        
    def on_connect(self, client, userdata, flags, rc):
        print(mqtt.connack_string(rc))
        if rc == 0:
            self.listen_on_topic(HEART_RATE_TOPIC, self._on_heart_rate_message)
            self.listen_on_topic(SMART_APPOINTMENTS_BOOK_TOPIC, self._on_book_appointment_message)
            self.listen_on_topic(SMART_APPOINTMENTS_NEW_TOPIC, self._on_new_appointment_message)
            
    def on_disconnect(self, client, userdata, rc):
        print(f'Disconnected. (code: {rc})')
    
    def on_subscribe(self, client, userdata, mid, granted_qos):
        print(f'Subscribed successfully with QoS: {granted_qos}')
            
    def on_message(self, client, userdata, message):
        print(f'QoS: [{message.qos}]\tTopic:\t[{message.topic}]\tReceived:\t[{message.payload}]')
       
    def _on_heart_rate_message(self, client, userdata, message):
        message_json = json.loads(message.payload)
        print(f'Topic: [{message.topic}] Message: [{message_json}]')

        self.h._connect()
        self.h._login(message_json["account"],message_json["key"])
        self.h._read_contract("access_contract_1588433638950.json")
        self.h.contract_access.add_heartrate(message_json["bpm"],message_json["timestamp"])


    def _on_new_appointment_message(self, client, userdata, message):
        message_json = json.loads(message.payload)
        print(f'Topic: [{message.topic}] Message: [{message_json}]')
        # todo
        
    def _on_book_appointment_message(self, client, userdata, message):
        message_json = json.loads(message.payload)
        print(f'Topic: [{message.topic}] Message: [{message_json}]')
        # todo
      
             
def _run(h):
    args = sys.argv
    try:
        if len(args) >= 3:
            listener = SmartMQTTListener(h,args[1], int(args[2]))
        else:
            listener = SmartMQTTListener(h)
    except ConnectionRefusedError as e:
        print(f'Failed to connect to MQTT. Default configuration is {DEFAULT_HOST}:{DEFAULT_PORT}')
        sys.exit(1)
        
    try:
        listener.loop_forever()
    except KeyboardInterrupt:
        print('Shutting down the proxy...')
    except Exception as e:
        print('Proxy has encountered an error.:', str(e))
    finally:
        listener.disconnect()


# if __name__ == '__main__':
#     _run()
         