import sys
import time
import json
import pprint

from solc import compile_source

current_time = lambda: int(round(time.time() * 1000))

# compile .sol
def _compile_source_file(file_path):
    with open(file_path,'r') as f:
        source = f.read()
    return compile_source(source)

# save contract address and ABI
def _log_deployment_result(result, file_path):
    with open(file_path, 'w') as f:
        json.dump(result, file_path, indent=4)

# build contract template
def _contract_deployment(w3, contract_compiled):
    return w3.eth.contract(
        abi=contract_compiled['abi'],
        bytecode=contract_compiled['bin'])

# build health data access contract and return its address and ABI on success
def build_health_data_access_contract(w3, data):
    path = 'contracts/HealthDataAccess.sol'
    compiled = _compile_source_file(path)
    contract_id, contract_compiled = compiled.popitem()
    
    deployment = _contract_deployment(w3, contract_compiled)
    estimate = deployment.constructor(data).estimateGas()
    print('The estimated cost of deploying access contract is {}'.format(estimate))
    try:
        tx_hash = deployment.constructor(data).transact()
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        
        result = {
            'contract_abi': contract_compiled['abi'],
            'contract_address': tx_receipt['contractAddress']
        }
        
        print('Deploy successful. Cost: {}'.format(tx_receipt['cumulativeGasUsed']))
        _log_deployment_result(result, 'cache/contract_{}.json'.format(current_time()))
        return result
    except Exception as e:
        print('Failed to deploy: {}'.format(str(e)))

class ContractLoader:
    def __init__(self, w3):
        self.w3 = w3
        
        
    def load_by_name(self, file_name):
        with open(f'cache/{file_name}', 'r') as f:
            result = json.load(f)
            
        try:
            self.contract_address = result['contract_address']
        except ValueError(f"Contract {file_name} is invalid."):
            raise
        
        contract_bytecode_length = len(self.w3.eth.getCode(self.contract_address).hex())
        try:
            assert (contract_bytecode_length > 4), f"Contract not deployed at {self.contract_address}"
        except AssertionError as e:
            print(str(e))
            raise
        
        self.contract_instance = self.w3.eth.contract(
            abi=result['contract_abi'],
            address=result['contract_address']
        )
        
        return self.contract_instance
            