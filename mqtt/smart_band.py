import sys
import time
import random
import json
import backoff
import asyncio
import paho.mqtt.client as mqtt

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1883
DEFAULT_QOS = 1
KEEPALIVE = 30
BACKOFF_INTERVAL = 1

HEART_RATE_TOPIC = 'smart/heart_rate'
MEASUREMENT_INTERVAL_MAX = 3 # 0-3 s delay in publishing measurement data

"""
Example of IoT Device which measures heart rate of the wearer
and publishes the data on a appropriate MQTT topic.
"""

def _timestamp_now():
    return int(round(time.time())*1000)

class SmartBand(mqtt.Client):
    def __init__(self, account_address, account_key, host=DEFAULT_HOST, port=DEFAULT_PORT):
        super().__init__(f'SmartBand_{_timestamp_now()}')
        self.account_address = account_address
        self.account_key = account_key
        self.connect_async(host, port, KEEPALIVE)
        
    def on_connect(self, client, userdata, flags, rc):
        print(mqtt.connack_string(rc))
        
    def on_disconnect(self, client, userdata, rc):
        print(f'Disconnected. ({rc})')
        
    def on_publish(self, client, userdata, mid):
        print(f'({mid}) Message published!')

    @backoff.on_exception(backoff.constant, Exception, interval=BACKOFF_INTERVAL)
    async def start_measurement(self):
        """Starts receiving measurement data and publishing it to the MQTT topic"""
        try:
            for measurement in self._heart_rate_measurement():
                self._publish_measurement(measurement)
                await asyncio.sleep(random.random() * MEASUREMENT_INTERVAL_MAX)
        except Exception as e:
            print(str(e))
            print(f'Exception: {type(e)} on publishing message, retrying after {BACKOFF_INTERVAL} second(s)')
            raise e
    
    def _publish_measurement(self, measurement):
        message = json.dumps(measurement)
        mid = self.publish(HEART_RATE_TOPIC, message, DEFAULT_QOS)[1]
        print(f'({mid}) Publishing message: {message}')
    
    def _heart_rate_measurement(self):
        BPM_MIN = 40
        BPM_MAX = 120
        BPM_STEP = 2
        while True:
            yield {
                'bpm' : random.randrange(BPM_MIN, BPM_MAX, BPM_STEP),
                'timestamp' : _timestamp_now(),
                'account' : self.account_address,
                'key' : self.account_key
            }


def load_credentials(file_path):
    try:
        with open(file_path, 'r') as f:
            credentials = json.loads(f.read())
            return credentials['address'], credentials['key']
    except Exception as e:
        print(f'Failed to login with credentials from {file_path} file')


def _run():
    args = sys.argv
    usage = f"Usage: python3 {args[0]} <credentials_file_path> [host] [port]"
    
    if len(args) < 2:
        print('Invalid number of arguments.')
        print(usage)    
        sys.exit(1)
    
    account_address, account_key = load_credentials(args[1])
    host = DEFAULT_HOST if len(args) < 3 else args[2]
    port = int(DEFAULT_PORT if len(args) < 4 else args[3])
    
    random.seed()
    try:
        band = SmartBand(account_address, account_key, host, port)
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
    _run()
    
        
