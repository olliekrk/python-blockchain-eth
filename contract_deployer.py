import sys
import time
import json
import pprint

from solcx import compile_source, get_solc_version, install_solc

SOLC_VERSION = 'v0.5.7'
install_solc(SOLC_VERSION)

current_time = lambda: int(round(time.time() * 1000))


# compile .sol
def _compile_source_file(file_path):
    with open(file_path+'.sol', 'r') as f:
        source = f.read()
    return compile_source(source)


# save contract address and ABI
def _log_deployment_result(result, file_path):
    with open(file_path, 'w') as f:
        json.dump(result, f, indent=4)


# build contract template
def _contract_deployment(w3, contract_compiled):
    return w3.eth.contract(
        abi=contract_compiled['abi'],
        bytecode=contract_compiled['bin'])


class ContractDeployer:
    def __init__(self, w3, account, private_key):
        self.w3 = w3
        self.account = account
        self.w3.eth.defaultAccount = account
        self.private_key = private_key

    # build health data access contract and return its address and ABI on success        
    def deploy_contract(self, data, path='contracts/HealthDataAccess'):
        compiled = _compile_source_file(path)
        contract_id, contract_compiled = compiled.popitem()

        deployment = _contract_deployment(self.w3, contract_compiled)
        estimate = deployment.constructor(data).estimateGas()
        print('The estimated cost of deploying access contract is {}'.format(estimate))
        try:
            tx = deployment.constructor(data).buildTransaction()
            tx_receipt = self._send_signed_transaction(tx)

            result = {
                'contract_abi': contract_compiled['abi'],
                'contract_address': tx_receipt['contractAddress']
            }

            cache_name = path.split('/')
            print('Deploy successful. Cost: {}'.format(tx_receipt['cumulativeGasUsed']))
            _log_deployment_result(result, 'cache/{}_{}.json'.format(cache_name[1], current_time()))
            return result
        except Exception as e:
            print('Failed to deploy: {}'.format(str(e)))

    def _sign_transaction(self, tx):
        return self.w3.eth.account.signTransaction(tx, self.private_key)

    def _send_signed_transaction(self, tx):
        tx.update({'nonce': self.w3.eth.getTransactionCount(self.account)})
        tx_signed = self._sign_transaction(tx)
        tx_hash = self.w3.eth.sendRawTransaction(tx_signed.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt


class ContractLoader:
    def __init__(self, w3):
        self.w3 = w3
        self.contract_address = None
        self.contract_abi = None
        self.contract_instance = None

    def load_contract(self, contract_address, contract_abi, cache=True, cache_name=None):
        self._validate_contract(contract_address)
        self.contract_instance = self.w3.eth.contract(abi=contract_abi, address=contract_address)
        if cache:
            if cache_name is None:
                cache_name = 'cache/loaded_contract_{}'.format(current_time())

            _log_deployment_result({'contract_abi': contract_abi, 'contract_address': contract_address}, cache_name)

        return self.contract_instance

    def load_by_name(self, file_name):
        with open(f'cache/{file_name}', 'r') as f:
            result = json.load(f)
        try:
            self.contract_address = result['contract_address']
            self.contract_abi = result['contract_abi']
        except ValueError(f"Contract {file_name} is invalid."):
            raise

        return self.load_contract(self.contract_address, self.contract_abi, False)

    def _validate_contract(self, contract_address):
        contract_bytecode_length = len(self.w3.eth.getCode(contract_address).hex())
        try:
            assert (contract_bytecode_length > 4), f"Contract not deployed at {self.contract_address}"
        except AssertionError as e:
            print(str(e))
            raise
