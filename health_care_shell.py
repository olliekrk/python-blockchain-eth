import cmd, sys
import threading
import json
from web3 import Web3
from contract_deployer import ContractDeployer, ContractLoader
from contract_handlers import HealthDataAccessContract, AppointmentBookingContract
from mqtt import SmartMQTTListener

NETWORK_URL = "http://127.0.0.1:7545"

# Convert a series of zero or more numbers to an argument tuple
parse = lambda arg: tuple(arg.split())

class HealthCareShell(cmd.Cmd):
    intro = 'Welcome to the Healthcare shell.   Type help or ? to list commands.\n'
    prompt = '>'

    w3 = None
    contract_loader = None
    deployer = None
    contract_access = None
    contract_booking = None
    health_data_access_handler = None
    appointment_booking_handler = None

    def _connect(self):
        try:
            self.w3 = Web3(Web3.HTTPProvider(NETWORK_URL))
            self.contract_loader = ContractLoader(self.w3)
            print("[0][Connection successful]")
        except:
            print("[1][Connection error]")

    def do_login(self, arg):
        """Login with given account and key"""
        if not self.w3:
            print("[1][Connect first!]")
            return

        args = parse(arg)
        if len(args) != 2:
            print("[1][Should give 2 args: address, key]")
        else:
            self._login(args[0], args[1])

    def do_login_file(self, arg):
        """Login with credentials from JSON file (i.e. credentials/example_credentials.json)"""
        args = parse(arg)
        if len(args) != 1:
            print("[1][Missing path to JSON credentials file]")
        else:
            try:
                with open(args[0], 'r') as f:
                    credentials = json.loads(f.read())
                    print(f'Using credentials: {credentials}')
                    self._login(credentials['address'], credentials['key'])
            except Exception as e:
                print(f'Failed to login with credentials from {args[0]} file')

    def do_connect(self, arg):
        """Connect to blockchain network"""
        self._connect()

    def do_add_heartrate(self, arg):
        """Adds new heartrate entry, gets 2 args: heartrate and timestamp"""
        if self.health_data_access_handler is None:
            print("[1][Not selected contract!]")
            return
        arguments = parse(arg)
        if len(arguments) != 2:
            print("[1][2 args expected: bpm and timestamp]")
        else:
            self.health_data_access_handler.add_heartrate(arguments[0], arguments[1])

    def do_get_my_data(self, arg):
        """Gets list of all heartrate data from contract selected previously"""
        if self.health_data_access_handler is None:
            print("[1][Not selected contract!]")
            return
        try:
            self.health_data_access_handler.get_data()
        except:
            print("[1][Error]")

    def do_get_my_last_data(self, arg):
        """Gets last heartrate data from contract selected previously"""
        if self.health_data_access_handler is None:
            print("[1][Not selected contract!]")
            return
        try:
            self.health_data_access_handler.get_last_data()
        except:
            print("[1][Error]")

    def do_grant_access(self, arg):
        """Grants access to heartrate data from contract selected previously. Takes account as argument"""
        if self.health_data_access_handler is None:
            print("[1][Not selected contract!]")
            return
        argument = parse(arg)
        if len(argument) == 0:
            print("[1][Not provided any argument]")
        else:
            self.health_data_access_handler.grant_access(argument[0])

    def do_revoke_access(self, arg):
        """Revokes access to heartrate data from contract selected previously. Takes account as argument"""
        if self.health_data_access_handler is None:
            print("[1][Not selected contract!]")
            return
        argument = parse(arg)
        if len(argument) == 0:
            print("[1][Not provided any argument]")
        else:
            self.health_data_access_handler.revoke_access(argument[0])

    def do_use_contract(self, arg):
        """Use contract from given file"""
        if not self.w3:
            print("[1][Not connected]")
            return

        file_name = parse(arg)
        if len(file_name) == 0:
            print("[1][Not provided any file]")
        else:
            self._read_contract(file_name[0])

    def do_deploy_appointment_booking_contract(self, arg):
        """Create new smart contract for logged account and deployes it. Also selects created contracs as currently
        used """
        args = parse(arg)
        data_argument = None
        if len(args) != 1:
            print("[1][Should give data argument")
            return
        else:
            data_argument = arg[0]

        if not self.deployer:
            print("[1][Login first!]")
            return
        try:
            result = self.deployer.deploy_contract(data_argument, 'AppointmentBooking')
            self.contract_booking = self.contract_loader.load_contract(result["contract_address"],
                                                                       result["contract_abi"],
                                                                       cache=False)
            self.appointment_booking_handler = AppointmentBookingContract(self.contract_access, self.w3)
            print("[0][Deployed and loaded contract]")
        except Exception as e:
            print(e)

    def do_deploy_data_access_contract(self, arg):
        """Create new smart contract for logged account and deploys it. Also selects created contract as currently used """
        args = parse(arg)
        data_argument = None
        if len(args) != 1:
            print("[1][Should give data argument")
            return
        else:
            data_argument = arg[0]

        if not self.deployer:
            print("[1][Login first!]")
            return
        try:
            result = self.deployer.deploy_contract(data_argument, 'HealthDataAccess')
            self.contract_access = self.contract_loader.load_contract(result["contract_address"], result["contract_abi"], cache=False)
            self.health_data_access_handler = HealthDataAccessContract(self.contract_access, self.w3)
            print("[0][Deployed and loaded contract]")
        except Exception as e:
            print("[1][Deploying unsuccessful]", str(e))

    def _read_contract(self, file_name):
        try:
            contract_type = file_name.split('_')[0]
            if contract_type == 'HealthDataAccess':
                self.contract_access = self.contract_loader.load_by_name(file_name)
                self.health_data_access_handler = HealthDataAccessContract(self.contract_access, self.w3)
            else:
                self.contract_booking = self.contract_loader.load_by_name(file_name)
                self.appointment_booking_handler = AppointmentBookingContract(self.contract_booking, self.w3)
            print("[0][Using given contract]")

        except Exception as e:
            print("[1][Could not read a contract from " + str(file_name) + "]")

    def _login(self, account, key):
        try:
            self.deployer = ContractDeployer(self.w3, str(account), str(key))
            print("[0][Login successful]")
        except:
            print("[1][Login unsuccessful]")


def start_smart_listener(health_care_shell):
    def heart_rate_callback(message):
        handler = health_care_shell.health_data_access_handler
        if handler is not None:
            try:
                handler.add_heartrate(message['bpm'], message['timestamp'])
            except Exception as e:
                print(f'Failed to send heart rate data to the blockchain: {str(e)}')


    def new_appointment_callback(message):
        handler = health_care_shell.appointment_booking_handler
        if handler is not None:
            try:
                handler.add_appointment(message['name'], message['timestamp'], message['price'], message['account'])
            except Exception as e:
                print(f'Failed to add an appointment: {str(e)}')


    def book_appointment_callback(message):
        handler = health_care_shell.appointment_booking_handler
        if handler is not None:
            try:
                handler.book_appointment(message['timestamp'], message['price'], message['account'])
            except Exception as e:
                print(f'Failed to book an appointment: {str(e)}')

    try:
        listener = SmartMQTTListener(
            new_appointment_callback=new_appointment_callback,
            book_appointment_callback=book_appointment_callback,
            heart_rate_callback=heart_rate_callback,
            verbose=False)
        listener.loop_forever()
    except ConnectionRefusedError as e:
        print('Failed to connect to MQTT.')
    except KeyboardInterrupt:
        print('Shutting down the listener...')
    except Exception as e:
        print('Listener has encountered an error.:', str(e))
    finally:
        listener.disconnect()


if __name__ == '__main__':
    health_care_shell = HealthCareShell()

    t = threading.Thread(target=start_smart_listener, args=(health_care_shell,))
    t.daemon = True
    t.start()

    health_care_shell.cmdloop()
