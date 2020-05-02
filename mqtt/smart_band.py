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
BACKOFF_INTERVAL = 2
MEASUREMENT_INTERVAL = 2
HEART_RATE_TOPIC = 'smart_iot/heart_rate'

"""
Example of IoT Device which measures heart rate of the wearer
and publishes the data on a appropriate MQTT topic.
"""

class SmartBand(mqtt.Client):
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        super().__init__(f'SmartBand_{int(time.time())}')
        self.connect(host, port, KEEPALIVE)
        
    @backoff.on_exception(backoff.constant, Exception, interval=BACKOFF_INTERVAL)
    async def start_measurement(self):
        """Starts receiving measurement data and publishing it to the MQTT topic"""
        try:
            for measurement in SmartBand._heart_rate_measurement():
                self._publish_measurement(measurement)
                await asyncio.sleep(MEASUREMENT_INTERVAL)
        except Exception as e:
            print(e)
            print(f'Exception: {type(e)} on publishing message, reconnecting after {BACKOFF_INTERVAL} second(s)')
            raise e
    
    def _publish_measurement(self, measurement):
        message = json.dumps(measurement)
        message_info = self.publish(HEART_RATE_TOPIC, message)
        print(f'Published: {message}')
    
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
        loop = asyncio.get_event_loop()
        loop.run_until_complete(band.start_measurement())
    except KeyboardInterrupt:
        print('Shutting down the device...')
    except Exception as e:
        print('Smart band has encountered an error.:', str(e))
    finally:
        band.disconnect()
        loop.close()
    
if __name__ == '__main__':
    run()
    
        
