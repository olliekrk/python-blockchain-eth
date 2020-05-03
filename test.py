import json
from web3 import Web3
from datetime import datetime



# Set up web3 connection with Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

web3.eth.defaultAccount = web3.eth.accounts[0]

abi = json.loads("""[
    {
      "constant": true,
      "inputs": [],
      "name": "name",
      "outputs": [
        {
          "name": "",
          "type": "string"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "doctor",
      "outputs": [
        {
          "name": "",
          "type": "address"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": false,
          "name": "date",
          "type": "uint256"
        },
        {
          "indexed": false,
          "name": "name",
          "type": "string"
        },
        {
          "indexed": false,
          "name": "price",
          "type": "uint256"
        },
        {
          "indexed": false,
          "name": "patient",
          "type": "address"
        }
      ],
      "name": "AppointmentCreated",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": false,
          "name": "date",
          "type": "uint256"
        },
        {
          "indexed": false,
          "name": "name",
          "type": "string"
        },
        {
          "indexed": false,
          "name": "price",
          "type": "uint256"
        },
        {
          "indexed": false,
          "name": "patient",
          "type": "address"
        }
      ],
      "name": "AppointmentBooked",
      "type": "event"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "printAppointments",
      "outputs": [
        {
          "name": "",
          "type": "string[]"
        },
        {
          "name": "",
          "type": "uint256[]"
        },
        {
          "name": "",
          "type": "uint256[]"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "name": "_name",
          "type": "string"
        },
        {
          "name": "_date",
          "type": "uint256"
        },
        {
          "name": "_price",
          "type": "uint256"
        }
      ],
      "name": "createAppointment",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "name": "_date",
          "type": "uint256"
        }
      ],
      "name": "bookAppointment",
      "outputs": [],
      "payable": true,
      "stateMutability": "payable",
      "type": "function"
    }
  ]""")

#Wy macie inny
address = web3.toChecksumAddress('0xC79811ccB67Cd4182038f96Fc3a0b1fd102eb5c1')
contract = web3.eth.contract(address=address, abi=abi)
# current date and time
now = datetime.now()

timestamp = datetime.timestamp(now)
print(datetime.fromtimestamp(1588238738).replace(microsecond=0, second=0, minute=0))
# print("timestamp =", timestamp)
print(datetime.timestamp(datetime.now().replace(microsecond=0, second=0, minute=0)))
print(web3.eth.accounts[1])
# print(contract.functions.createAppointment("dermatolog",int(timestamp),10).transact())
# print(contract.functions.bookAppointment(int(timestamp)).transact({'from': web3.eth.accounts[1],'value': web3.toWei(2,'ether')}))
# print(contract.functions.printAppointments().call())



class AppointmentBooking:

    def __init__(self, contract, w3):
        self.contract = contract
        self.w3 = w3

    def add_appointment(self, name, timestamp, price):
        try:
            date = datetime.fromtimestamp(timestamp).replace(microsecond=0, second=0, minute=0)
            hash_tx = self.contract.functions.createAppointment(name, int(datetime.timestamp(date)),price).transact()
            receip = self.w3.eth.waitForTransactionReceipt(hash_tx)

            print(receip)
        except Exception as e:
            print(e)
            print("[1][Error!]")

    def book_appointment(self, timestamp, price, account):
        try:
            date = datetime.fromtimestamp(timestamp).replace(microsecond=0, second=0, minute=0)
            result = self.contract.functions.bookAppointment(datetime.timestamp(date)).transact({'from': account,'value': web3.toWei(price,'ether')})
            print(result)
        except Exception as e:
            print(e)
            print("[1][Error!]")