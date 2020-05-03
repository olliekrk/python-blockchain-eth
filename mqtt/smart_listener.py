import sys
import time
import json
import paho.mqtt.client as mqtt
from mqtt_defaults import DEFAULT_HOST, DEFAULT_PORT, KEEPALIVE, DEFAULT_QOS, HEART_RATE_TOPIC, SMART_APPOINTMENTS_BOOK_TOPIC, SMART_APPOINTMENTS_NEW_TOPIC

def _timestamp_now():
    return int(round(time.time())*1000)


class SmartMQTTListener(mqtt.Client):
    def __init__(self,
                 host=DEFAULT_HOST, 
                 port=DEFAULT_PORT, 
                 heart_rate_callback=None,
                 new_appointment_callback=None,
                 book_appointment_callback=None):
        super().__init__(f'SmartListener_{_timestamp_now()}')
        self.connect_async(host, port, KEEPALIVE)
        self.heart_rate_callback = heart_rate_callback
        self.new_appointment_callback = new_appointment_callback
        self.book_appointment_callback = book_appointment_callback
        
    def listen_on_topic(self, topic, callback, qos=DEFAULT_QOS):
        self.message_callback_add(topic, callback)
        print(f'Subscribing to the [{topic}] topic...')
        self.subscribe(topic, qos)
        
    def on_connect(self, client, userdata, flags, rc):
        print(mqtt.connack_string(rc))
        if rc == 0:
            self.listen_on_topic(HEART_RATE_TOPIC, self.default_callback(self.heart_rate_callback))
            self.listen_on_topic(SMART_APPOINTMENTS_BOOK_TOPIC, self.default_callback(self.book_appointment_callback))
            self.listen_on_topic(SMART_APPOINTMENTS_NEW_TOPIC, self.default_callback(self.new_appointment_callback))
            
    def on_disconnect(self, client, userdata, rc):
        print(f'Disconnected. (code: {rc})')
    
    def on_subscribe(self, client, userdata, mid, granted_qos):
        print(f'Subscribed successfully with QoS: {granted_qos}')
            
    def on_message(self, client, userdata, message):
        print(f'QoS: [{message.qos}]\tTopic:\t[{message.topic}]\tReceived:\t[{message.payload}]')
    
    def default_callback(self, callback):
        def handler(client, userdata, message):
            message_json = json.loads(message.payload)
            print(f'Topic: [{message.topic}] Message: [{message_json}]')
            if self.callback is not None:
                self.callback(message_json)
        return handler
      
             
def run():
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
        print('Shutting down the listener...')
    except Exception as e:
        print('Listener has encountered an error.:', str(e))
    finally:
        listener.disconnect()


if __name__ == '__main__':
    print("""
          Running Smart Listener as a separate application.
          Only listening to topics and logging received messages.
          """)
    run()