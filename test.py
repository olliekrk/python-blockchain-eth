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
          "type": "string"
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
        },
        {
          "indexed": false,
          "name": "doctor",
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
          "type": "string"
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
        },
        {
          "indexed": false,
          "name": "doctor",
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
          "type": "string[]"
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
          "type": "string"
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
          "type": "string"
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
address = web3.toChecksumAddress('0x6271DC93CdC42eaf6ec5dF5D25807dFFac7011ED')
contract = web3.eth.contract(address=address, abi=abi)
# current date and time
now = datetime.now()

# timestamp = datetime.timestamp(now)
# print("timestamp =", timestamp)

print(contract.functions.createAppointment("dermatolog","20-08-2019",10).transact())
print(contract.functions.bookAppointment("20-08-2019").transact({'from': web3.eth.accounts[1],'value': web3.toWei(2,'ether')}))
print(contract.functions.printAppointments().call())