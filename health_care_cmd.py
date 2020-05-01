import cmd, sys
import contract_deployer
from connector import Web3Connector, NETWORK_URL


class HealthDataAccessContract:

    def __init__(self, contract):
        self.contract = contract


class HealthCareShell(cmd.Cmd):
    intro = 'Welcome to the Healthcare shell.   Type help or ? to list commands.\n'
    prompt = '>'
    # file = None

    private_key = None
    w3 = None
    contract = None
    contact_loader = None
    contract_access = None

    def _read_key(self, file_name):
        try:
            file = open(file_name)
            self.private_key = file.readline()
        except:
            print("[0][Could not read a key from " + str(file_name) + "]")

    def _connect(self):
        try:
            self.w3 = Web3Connector(NETWORK_URL)
            print("[0][Connection successful]")
            print(self.w3)
        except:
            print("[1][Connection error]")

    def do_get_key(self, arg):
        """Get private key from provided file"""
        file_name = parse(arg)
        if len(file_name) == 0:
            print("[1][Not provided any file]")
        else:
            self._read_key(file_name[0])

    def do_connect(self):
        """Connect to network"""
        self._connect()

    def do_add_heartrate(self):
        pass

    def do_get_my_data(self):
        pass

    def do_grant_access(self):
        pass

    def do_revoke_access(self):
        pass

    def use_contract(self, arg):
        """Use contract from given file"""
        if not self.w3:
            print("[1][Not connected]")
            return

        file_name = parse(arg)
        if len(file_name) == 0:
            print("[1][Not provided any file]")
        else:
            self._read_contract(file_name[0])

    def _read_contract(self, file_name):
        try:
            if not self.contact_loader:
                self.contact_loader = contract_deployer.ContractLoader(self.w3)
            self.contract = self.contact_loader.load_by_name(file_name)
            self.contract_access = HealthDataAccessContract(self.contract)
        except:
            print("[0][Could not read a contract from " + str(file_name) + "]")


def parse(arg):
    """Convert a series of zero or more numbers to an argument tuple"""
    return tuple(arg.split())


if __name__ == '__main__':
    HealthCareShell().cmdloop()
