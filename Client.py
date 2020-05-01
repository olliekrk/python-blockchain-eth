import cmd, sys
from turtle import *
from app import Web3Connector
from app import NETWORK_URL


class HealthCareShell(cmd.Cmd):
    intro = 'Welcome to the turtle shell.   Type help or ? to list commands.\n'
    prompt = '>'
    # file = None

    private_key = None
    w3 = None

    def _read_file(self, file_name):
        try:
            file = open(file_name)
            self.private_key = file.readline()
        except:
            print("Could not read a key from " + str(file_name))

    def _login(self):
        try:
            self.w3 = Web3Connector(NETWORK_URL)
            print("connection successful!")
            print(self.w3)
        except:
            print("Connecton error!")


    def do_login(self, arg):
        'Login to smart contract using key in provided file'
        file_name = parse(arg)
        if len(file_name) == 0:
            print("Not provided any file!")
        else:
            self._read_file(file_name[0])
            if self.private_key:
                self._login()

    def do_add_heartrate(self):
        pass

    def do_get_my_data(self):
        pass

    def do_grant_access(self):
        pass

    def do_revoke_access(self):
        pass

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(arg.split())


if __name__ == '__main__':
    HealthCareShell().cmdloop()
