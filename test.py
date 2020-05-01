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
      "type": "function",
      "signature": "0x06fdde03"
    },
    {
      "inputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "constructor",
      "signature": "constructor"
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
      "type": "event",
      "signature": "0xd4b90129ae99e8ad73ce5e9db530a6b1bd0595b15666ec560b427d56545d4db0"
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
      "type": "event",
      "signature": "0x8c888748e05b7e429cf1a1c89cdcee30cf7a53e925cce5c76a1c307617fc036e"
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
      "type": "function",
      "signature": "0x9053afdb"
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
      "type": "function",
      "signature": "0x85ab23c9"
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
      "type": "function",
      "signature": "0x36161283"
    }
  ]""")

#Wy macie inny
address = web3.toChecksumAddress('0x3f27b7A16e0bF04B88D3532aBc1C89991EE3e95A')
contract = web3.eth.contract(address=address, abi=abi)
# current date and time
now = datetime.now()

# timestamp = datetime.timestamp(now)
# print("timestamp =", timestamp)

print(contract.functions.createAppointment("dermatolog","20-08-2019",10).transact())
print(contract.functions.bookAppointment("20-08-2019").transact({'from': web3.eth.accounts[0],'value': web3.toWei(2,'ether')}))
print(contract.functions.printAppointments().call())