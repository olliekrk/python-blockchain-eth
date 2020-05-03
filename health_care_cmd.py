import cmd, sys
import threading
from datetime import datetime
import contract_deployer
from connector import Web3Connector, NETWORK_URL
from mqtt import SmartMQTTListener

# Convert a series of zero or more numbers to an argument tuple
parse = lambda arg: tuple(arg.split())

class AppointmentBooking:
    
    def __init__(self, contract, w3):
        self.contract = contract
        self.w3 = w3

    def add_appointment(self, name, timestamp, price):
        try:
            date = datetime.fromtimestamp(timestamp).replace(microsecond=0, second=0, minute=0)
            hash_tx = self.contract.functions.createAppointment(name, int(datetime.timestamp(date)), price).transact()
            receip = self.w3.eth.waitForTransactionReceipt(hash_tx)

            print(receip)
        except Exception as e:
            print(e)
            print("[1][Error!]")

    def book_appointment(self, timestamp, price, account):
        try:
            date = datetime.fromtimestamp(timestamp).replace(microsecond=0, second=0, minute=0)
            result = self.contract.functions.bookAppointment(datetime.timestamp(date)).transact(
                {'from': account, 'value': self.web3.toWei(price, 'ether')})
            print(result)
        except Exception as e:
            print(e)
            print("[1][Error!]")

    def print_appointments(self):
        print(self.contract.functions.printAppointments().call())


class HealthDataAccessContract:
    
    def __init__(self, contract, w3):
        self.contract = contract
        self.w3 = w3

    def add_heartrate(self, heartrate, date):
        try:
            hash_tx = self.contract.functions.addMeasurement(int(heartrate), int(date)).transact()
            receip = self.w3.eth.waitForTransactionReceipt(hash_tx)

            print(receip)
        except Exception as e:
            print(e)
            print("[1][Error!]")

    def get_data(self):
        try:
            result = self.contract.functions.getMeasurements().call()
            print(result)
        except Exception as e:
            print(e)
            print("[1][Error!]")

    def get_last_data(self):
        try:
            result = self.contract.functions.getLastMeasurement().call()
            print(result)
        except Exception as e:
            print(e)
            print("[1][Error!]")

    def grant_access(self, argument):
        try:
            hash_tx = self.contract.functions.grantAccess(argument).transact()
            receip = self.w3.eth.waitForTransactionReceipt(hash_tx)

            print(receip)
        except Exception as e:
            print(e)
            print("[1][Error!]")

    def revoke_access(self, argument):
        try:
            hash_tx = self.contract.functions.revokeAccess(argument).transact()
            receip = self.w3.eth.waitForTransactionReceipt(hash_tx)

            print(receip)
        except Exception as e:
            print(e)
            print("[1][Error!]")


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
            self.w3 = Web3Connector(NETWORK_URL)
            self.contract_loader = contract_deployer.ContractLoader(self.w3.w3)
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
            result = self.deployer.deploy_contract(data_argument, 'contracts/AppointmentBooking')
            self.contract_booking = self.contract_loader.load_contract(result["contract_address"],
                                                                       result["contract_abi"])
            self.appointment_booking_handler = AppointmentBooking(self.contract_access, self.w3.w3)
            print("[0][Deployed and loaded contract]")
        except Exception as e:
            print(e)

    def do_deploy_data_access_contract(self, arg):
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
            result = self.deployer.deploy_contract(data_argument)
            self.contract_access = self.contract_loader.load_contract(result["contract_address"], result["contract_abi"])
            self.health_data_access_handler = HealthDataAccessContract(self.contract_access, self.w3.w3)
            print("[0][Deployed and loaded contract]")
        except:
            print("[1][Deploying unsuccessful]")

    def _read_contract(self, file_name):
        try:
            contract_type = file_name.split('_')[0]
            if contract_type == 'HealthDataAccess':
                self.contract_access = self.contract_loader.load_by_name(file_name)
                self.health_data_access_handler = HealthDataAccessContract(self.contract_access, self.w3.w3)
            else:
                self.contract_booking = self.contract_loader.load_by_name(file_name)
                self.appointment_booking_handler = AppointmentBooking(self.contract_booking, self.w3.w3)
            print("[0][Using given contract]")

        except Exception as e:
            print("[1][Could not read a contract from " + str(file_name) + "]")

    def _login(self, account, key):
        try:
            self.deployer = contract_deployer.ContractDeployer(self.w3.w3, str(account), str(key))
            print("[0][Login successful]")
        except:
            print("[1][Login unsuccessful]")



def start_smart_listener(health_care):
    def heart_rate_callback(message):
        try:
            health_care.do_add_heartrate(message['bpm'], message['timestamp'])
        except Exception as e:
            print(f'Failed to send heart rate data to the blockchain: {str(e)}')
    
    try:
        listener = SmartMQTTListener(heart_rate_callback=heart_rate_callback)
        listener.loop_forever()
    except ConnectionRefusedError as e:
        print(f'Failed to connect to MQTT. Default configuration is {DEFAULT_HOST}:{DEFAULT_PORT}')
    except KeyboardInterrupt:
        print('Shutting down the listener...')
    except Exception as e:
        print('Listener has encountered an error.:', str(e))
    finally:
        listener.disconnect()
    

if __name__ == '__main__':
    health_care = HealthCareShell()
    
    t = threading.Thread(target=start_smart_listener, args=(health_care,))
    t.daemon = True
    t.start()

    health_care.cmdloop()
