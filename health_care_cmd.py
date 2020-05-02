import cmd, sys

import contract_deployer
from connector import Web3Connector, NETWORK_URL


class HealthDataAccessContract:

    def __init__(self, contract):
        self.contract = contract

    def add_heartrate(self, heartrate, date):
        result = self.contract.functions.addMeasurement(int(heartrate), int(date)).call()
        print(result)

    def get_data(self):
        result = self.contract.functions.getMeasurements().call()
        print(result)

    def get_last_data(self):
        result = self.contract.functions.getLastMeasurement().call()
        print(result)

    def grant_access(self, argument):
        result = self.contract.functions.grantAccess(argument).call()
        print(result)

    def revoke_access(self, argument):
        result = self.contract.functions.revokeAccess(argument).call()
        print(result)


class HealthCareShell(cmd.Cmd):
    intro = 'Welcome to the Healthcare shell.   Type help or ? to list commands.\n'
    prompt = '>'
    # file = None

    w3 = None
    contract = None
    contract_loader = None
    contract_access = None
    deployer = None

    def _connect(self):
        try:
            self.w3 = Web3Connector(NETWORK_URL)
            self.contract_loader = contract_deployer.ContractLoader(self.w3.w3)
            print("[0][Connection successful]")
            print(self.w3)
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
        """Connect to network"""
        self._connect()

    def do_add_heartrate(self, arg):
        if self.contract_access is None:
            print("[1][Not selected contract!]")
            return
        arguments = parse(arg)
        if len(arguments) != 2:
            print("[1][2 args expected: bpm and timestamp]")
        else:
            self.contract_access.add_heartrate(arguments[0], arguments[1])

    def do_get_my_data(self, arg):
        if self.contract_access is None:
            print("[1][Not selected contract!]")
            return
        try:
            self.contract_access.get_data()
        except:
            print("[1][Error]")
    def do_get_my_last_data(self, arg):
        if self.contract_access is None:
            print("[1][Not selected contract!]")
            return
        try:
            self.contract_access.get_last_data()
        except:
            print("[1][Error]")

    def do_grant_access(self, arg):
        if self.contract_access is None:
            print("[1][Not selected contract!]")
            return
        argument = parse(arg)
        if len(argument) == 0:
            print("[1][Not provided any argument]")
        else:
            self.contract_access.grant_access(argument)

    def do_revoke_access(self, arg):
        if self.contract_access is None:
            print("[1][Not selected contract!]")
            return
        argument = parse(arg)
        if len(argument) == 0:
            print("[1][Not provided any argument]")
        else:
            self.contract_access.revoke_access(argument)

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
            print("[0][Using given contract]")

    def do_deploy_data_access_contract(self, arg):
        if not self.deployer:
            print("[1][Login first!]")
            return

        result = self.deployer.deploy_data_access_contract("Magic_String")
        self.contract = self.contract_loader.load_contract(result["contract_address"], result["contract_abi"])
        self.contract_access = HealthDataAccessContract(self.contract)
        print("[0][Deployed and loaded contract]")

    def _read_contract(self, file_name):
        try:
            self.contract = self.contract_loader.load_by_name(file_name)
            self.contract_access = HealthDataAccessContract(self.contract)
        except Exception as e:
            print(e)
            print("[0][Could not read a contract from " + str(file_name) + "]")

    def _login(self, account, key):
        #print(str(account))
        #print(str(key))
        self.deployer = contract_deployer.ContractDeployer(self.w3.w3, str(account), str(key))
        print("[0][Login succesfull]")

def parse(arg):
    """Convert a series of zero or more numbers to an argument tuple"""
    return tuple(arg.split())


if __name__ == '__main__':
    HealthCareShell().cmdloop()
