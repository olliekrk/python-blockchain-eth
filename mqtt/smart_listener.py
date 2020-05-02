import sys
import time
import json
import paho.mqtt.client as mqtt
from mqtt_defaults import *

def _timestamp_now():
    return int(round(time.time())*1000)


class SmartMQTTListener(mqtt.Client):
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        super().__init__(f'SmartListener_{_timestamp_now()}')
        self.connect_async(host, port, KEEPALIVE)
        
    def listen_for_heart_rate_data(self, qos=DEFAULT_QOS):
        self.message_callback_add(HEART_RATE_TOPIC, self._on_heart_rate_message)
        print(f'Subscribing to the [{HEART_RATE_TOPIC}] topic...')
        self.subscribe(HEART_RATE_TOPIC, qos)
        
    def listen_for_new_appointments(self, qos=DEFAULT_QOS):
        self.message_callback_add(SMART_APPOINTMENTS_NEW_TOPIC, self._on_new_appointment_message)
        print(f'Subscribing to the [{SMART_APPOINTMENTS_NEW_TOPIC}] topic...')
        self.subscribe(SMART_APPOINTMENTS_NEW_TOPIC, qos)
    
    def listen_for_book_appointments(self, qos=DEFAULT_QOS):
        self.message_callback_add(SMART_APPOINTMENTS_BOOK_TOPIC, self._on_book_appointment_message)
        print(f'Subscribing to the [{SMART_APPOINTMENTS_BOOK_TOPIC}] topic...')
        self.subscribe(SMART_APPOINTMENTS_BOOK_TOPIC, qos)
    
    def on_connect(self, client, userdata, flags, rc):
        print(mqtt.connack_string(rc))
        if rc == 0:
            self.listen_for_heart_rate_data()
            self.listen_for_new_appointments()
            self.listen_for_book_appointments()
            
    def on_disconnect(self, client, userdata, rc):
        print(f'Disconnected. (code: {rc})')
    
    def on_subscribe(self, client, userdata, mid, granted_qos):
        print(f'Subscribed successfully with QoS: {granted_qos}')
            
    def on_message(self, client, userdata, message):
        print(f'QoS: [{message.qos}]\tTopic:\t[{message.topic}]\tReceived:\t[{message.payload}]')
       
    def _on_heart_rate_message(self, client, userdata, message):
        message_json = json.loads(message.payload)
        print(f'Topic: [{message.topic}] Message: [{message_json}]')
        # todo: this should push data to the smart contract
        
    def _on_new_appointment_message(self, client, userdata, message):
        message_json = json.loads(message.payload)
        print(f'Topic: [{message.topic}] Message: [{message_json}]')
        # todo
        
    def _on_book_appointment_message(self, client, userdata, message):
        message_json = json.loads(message.payload)
        print(f'Topic: [{message.topic}] Message: [{message_json}]')
        # todo
      
             
def _run():
    args = sys.argv
    try:
        if len(args) >= 3:
            listener = SmartMQTTListener(args[1], int(args[2]))
        else:
            listener = SmartMQTTListener()
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


if __name__ == '__main__':
    _run()
         