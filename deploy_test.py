import json
import os
import contract_deployer
from web3 import Web3


NETWORK_URL = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(NETWORK_URL))

build_result = contract_deployer.build_health_data_access_contract(web3, "*Magic String*")
print(build_result)

if build_result is not None:
    contract = web3.eth.contract(address=build_result['contract_address'], abi=build_result['contract_abi'])
    print(contract)
