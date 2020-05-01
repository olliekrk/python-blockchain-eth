import json
import os
from contract_deployer import ContractDeployer
from web3 import Web3


NETWORK_URL = "http://127.0.0.1:7545"
ACCOUNT = "0x08526EaA9f719b374c0CCc381D3486974f5F28bD"
KEY = "0x9b0fc233b3d3cc5097552e0d09085884413f5ec1c46b2d3a50f7c6c62e210cbb"

web3 = Web3(Web3.HTTPProvider(NETWORK_URL))

deployer = ContractDeployer(web3, ACCOUNT, KEY)
deploy_result = deployer.deploy_data_access_contract("*Magic String*")
print(deploy_result)

if deploy_result is not None:
    contract = web3.eth.contract(address=deploy_result['contract_address'], abi=deploy_result['contract_abi'])
    print(contract)
