# python-blockchain-eth
> Short university task using blockchain platform & smart contracts on Ethereum network.

## Requirements:
* Deploy a local ethereum network on localhost, port 7545 (i.e. with Ganache)
* Deploy a local mosquitto server on localhost, port 1883
* Install the requirements `python3 -m pip install -r requirements.txt`

## Usage:
> TODO

#### Tools:
* Python (version >= 3.6.9)
* Web3.py
* Ganache - Local Ethereum Network
* [Remix IDE](https://remix.ethereum.org/) - IDE for writing Smart Contracts
* Solidity
* [Truffle.js](https://www.trufflesuite.com/)
* mosquitto MQTT server
* paho-mqtt library

#### How to run mosquitto
```
mosquitto -c mosquitto.conf
```

#### How to run Ganache
```
ganache-cli -p 7545
```

##### How to compile Smart Contracts
```
truffle compile [--network development]
```

##### How to deploy Smart Contracts on Ganache
```
truffle deploy [--network development]
```

#### Misc
```
truffle help <command>
```

##### Contributors

* [Rafał Juraszek](http://github.com/RafalJuraszek)
* [Olgierd Królik](http://github.com/olliekrk)
* [Wiktor Pawłowski](http://github.com/wiktor145)
