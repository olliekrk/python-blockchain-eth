import sys
import time
import json
import cmd2
import argparse
import paho.mqtt.client as mqtt

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1883
DEFAULT_QOS = 1
KEEPALIVE = 30

SMART_APPOINTMENTS_NEW_TOPIC = 'smart/appointment/new'
SMART_APPOINTMENTS_BOOK_TOPIC = 'smart/appointment/book'

def _timestamp_now():
    return int(round(time.time())*1000)

class SmartTablet(mqtt.Client):
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        super().__init__(f'SmartTablet_{_timestamp_now()}')
        self.connect_async(host, port, KEEPALIVE)
            
    def on_connect(self, client, userdata, flags, rc):
        print(mqtt.connack_string(rc))
        
    def on_disconnect(self, client, userdata, rc):
        print(f'Disconnected. ({rc})')
        
    def on_publish(self, client, userdata, mid):
        print(f'({mid}) Message published!')
        
    def new_appointment(self, appointment):
        message = json.dumps(appointment)
        mid = self.publish(SMART_APPOINTMENTS_NEW_TOPIC, message, DEFAULT_QOS)[1]
        print(f'({mid}) Publishing new appointment: {message}')
    
    def book_appointment(self, appointment):
        message = json.dumps(appointment)
        mid = self.publish(SMART_APPOINTMENTS_BOOK_TOPIC, message, DEFAULT_QOS)[1]
        print(f'({mid}) Booking appointment: {message}')
 

def _login_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', required=True, action='store', help='Address of the account to log into')
    parser.add_argument('-k', '--key', required=True, action='store', help='Private key of the account')
    return parser


def _login_file_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--credentials', required=True, action='store', help='Load using JSON credentials file')
    return parser


def _new_appointment_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', required=True, action='store', help='Name of the appointment')
    parser.add_argument('-p', '--price', required=True, type=int, action='store', help='Gas price of the appointment')
    parser.add_argument('-t', '--timestamp', required=True, type=int, action='store', help='Timestamp of the appointment')
    return parser
        

def _book_appointment_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--timestamp', required=True, type=int, action='store', help='Timestamp of the appointment')
    return parser               
        
class SmartTabletCmd(cmd2.Cmd):
    prompt = 'e-health-booking>'
    
    def __init__(self, tablet):
        super().__init__()
        self.tablet = tablet
        self.logged_in = False
        
    @cmd2.with_argparser(_login_parser())
    def do_login(self, args):
        """Sign in to existing blockchain account"""
        self.account_address = args.address
        self.account_key = args.key
        self.logged_in = True
        
    @cmd2.with_argparser(_login_file_parser())
    def do_login_file(self, args):
        """Sign in to existing blockchain account using file with credentials"""
        try:
            with open(args.credentials, 'r') as f:
                credentials = json.loads(f.read())
                self.account_address = credentials['address']
                self.account_key = credentials['key']
                self.logged_in = True
        except Exception as e:
            print(f'Failed to sign in using credentials file!', str(e))
    
    @cmd2.with_argparser(_new_appointment_parser())
    def do_new_appointment(self, args):
        """Creates and broadcasts a new appointment"""
        if self.logged_in:
            self.tablet.new_appointment({
                'name' : args.name,
                'timestamp' : args.timestamp,
                'price' : args.price,
                'account' : self.account_address,
                'key' : self.account_key    
            })
        else:
            print('Please sign in first!')
            
    
    @cmd2.with_argparser(_book_appointment_parser())
    def do_book_appointment(self, args):
        """Books an appointment if available"""
        if self.logged_in:
            self.tablet.book_appointment({
                'timestamp' : args.timestamp,
                'account' : self.account_address,
                'key' : self.account_key
            })
        else:
            print('Please sign in first!')
            
    def do_logout(self, args):
        """End client session and forget given credentials"""
        self.logged_in = False
        self.account_address = None
        self.account_key = None
    

def _run():
    args = sys.argv
    try:
        if len(args) >= 3:
            tablet = SmartTablet(args[1], int(args[2]))
        else:
            tablet = SmartTablet()
    except ConnectionRefusedError as e:
        print(f'Failed to connect to MQTT. Default configuration is {DEFAULT_HOST}:{DEFAULT_PORT}')
        sys.exit(1)
        
    cmd = SmartTabletCmd(tablet)
        
    try:
        tablet.loop_start()
        cmd.cmdloop()
    except KeyboardInterrupt:
        print('Shutting down the device...')
    except Exception as e:
        print('Smart Tablet has encountered an error.:', str(e))
    finally:
        tablet.disconnect()
        tablet.loop_stop()
    
if __name__ == '__main__':
    _run()
    
        
