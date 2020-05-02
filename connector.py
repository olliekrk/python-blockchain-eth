import json
import os
from web3 import Web3

NETWORK_URL = "http://127.0.0.1:7545"


class Web3Connector:
    def __init__(self, provider_url):
        self.provider_url = provider_url
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
    
    def get_balance(self, account, unit='ether'):
        balance = self.w3.eth.getBalance(account)
        return self.w3.fromWei(balance, unit)
    
    def get_contract(self, address, abi):
        return self.w3.eth.contract(address, abi=abi)
    
    def build_tx(self, account1, account2, value, gas, gasPrice):
        return {
            'nonce': self.w3.eth.getTransactionCount(account1),
            'to': account2,
            'value': self.w3.toWei(value, 'ether'),
            'gas': gas, # unit
            'gasPrice': self.w3.toWei(gasPrice, 'gwei') # price per unit
        }  
        
    def sign_tx(self, tx, private_key):
        return self.w3.eth.account.signTransaction(tx, private_key)
    
    def send_tx(self, tx):
        try:
            tx_hash = self.w3.eth.sendRawTransaction(tx.rawTransaction)
            return Web3.toHex(tx_hash)
        except Exception as e:
            print ('Failed to commit the transaction due to: {}'.format(str(e)))
            return None