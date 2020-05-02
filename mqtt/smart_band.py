import sys
import time
import random
import json
import backoff
import asyncio
import paho.mqtt.client as mqtt

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1883
KEEPALIVE = 30
BACKOFF_INTERVAL = 1
MEASUREMENT_INTERVAL_MAX = 5 # [0, 1) * MAX
HEART_RATE_TOPIC = 'heart_rate'

"""
Example of IoT Device which measures heart rate of the wearer
and publishes the data on a appropriate MQTT topic.
"""

def _on_connect(client, userdata, flags, rc):
    print('Connection success!' if rc == 0 else f'Connection failure: ({rc})')

def _on_disconnect(client, userdata, rc):
    print(f'Disconnected. ({rc})')
    
def _on_publish(client, userdata, mid):
    print(f'Published message no. {mid}!')

class SmartBand(mqtt.Client):
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        super().__init__(f'SmartBand_{int(time.time())}')
        self.on_connect = _on_connect
        self.on_disconnect = _on_disconnect
        self.on_publish = _on_publish
        self.connect_async(host, port, KEEPALIVE)
    
    
    @backoff.on_exception(backoff.constant, Exception, interval=BACKOFF_INTERVAL)
    async def start_measurement(self):
        """Starts receiving measurement data and publishing it to the MQTT topic"""
        try:
            for measurement in SmartBand._heart_rate_measurement():
                self._publish_measurement(measurement)
                await asyncio.sleep(random.random() * MEASUREMENT_INTERVAL_MAX)
        except Exception as e:
            print(str(e))
            print(f'Exception: {type(e)} on publishing message, retrying after {BACKOFF_INTERVAL} second(s)')
            raise e
    
    def _publish_measurement(self, measurement):
        message = json.dumps(measurement)
        message_info = self.publish(topic=HEART_RATE_TOPIC, payload=message, qos=1)
        print(f'Publishing... {message}')
    
    @classmethod
    def _heart_rate_measurement(cls):
        while True:
            yield {
                'bpm' : random.randrange(40, 120, 2),
                'timestamp' : int(round(time.time()) * 1000)
            }


def run():
    random.seed()
    args = sys.argv
    try:
        if len(args) >= 3:
            band = SmartBand(args[1], int(args[2]))
        else:
            band = SmartBand()
    except ConnectionRefusedError as e:
        print(f'Failed to connect to MQTT. Default configuration is {DEFAULT_HOST}:{DEFAULT_PORT}')
        sys.exit(1)
        
    try:
        band.loop_start()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(band.start_measurement())
    except KeyboardInterrupt:
        print('Shutting down the device...')
    except Exception as e:
        print('Smart band has encountered an error.:', str(e))
    finally:
        band.disconnect()
        band.loop_stop()
        loop.close()
    
if __name__ == '__main__':
    run()
    
        
