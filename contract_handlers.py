from datetime import datetime

class AppointmentBookingContract:
    
    def __init__(self, contract, w3):
        self.contract = contract
        self.w3 = w3

    def add_appointment(self, name, timestamp, price):
        try:
            date = datetime.fromtimestamp(timestamp).replace(microsecond=0, second=0, minute=0)
            hash_tx = self.contract.functions.createAppointment(name, int(datetime.timestamp(date)), price).transact()
            receipt = self.w3.eth.waitForTransactionReceipt(hash_tx)

            print(receipt)
        except Exception as e:
            print(e)
            print("[1][Error!]")

    def book_appointment(self, timestamp, price, account):
        try:
            date = datetime.fromtimestamp(timestamp).replace(microsecond=0, second=0, minute=0)
            result = self.contract.functions.bookAppointment(datetime.timestamp(date)).transact(
                {'from': account, 'value': self.web3.toWei(price, 'ether')})
            print(result)
        except Exception as e:
            print(e)
            print("[1][Error!]")

    def print_appointments(self):
        print(self.contract.functions.printAppointments().call())


class HealthDataAccessContract:
    
    def __init__(self, contract, w3):
        self.contract = contract
        self.w3 = w3

    def add_heartrate(self, heartrate, date):
        try:
            hash_tx = self.contract.functions.addMeasurement(int(heartrate), int(date)).transact()
            receipt = self.w3.eth.waitForTransactionReceipt(hash_tx)
            print(receipt)
        except Exception as e:
            print(e)
            print("[1][Error!]")

    def get_data(self):
        try:
            result = self.contract.functions.getMeasurements().call()
            print(result)
        except Exception as e:
            print(e)
            print("[1][Error!]")

    def get_last_data(self):
        try:
            result = self.contract.functions.getLastMeasurement().call()
            print(result)
        except Exception as e:
            print(e)
            print("[1][Error!]")

    def grant_access(self, argument):
        try:
            hash_tx = self.contract.functions.grantAccess(argument).transact()
            receipt = self.w3.eth.waitForTransactionReceipt(hash_tx)

            print(receipt)
        except Exception as e:
            print(e)
            print("[1][Error!]")

    def revoke_access(self, argument):
        try:
            hash_tx = self.contract.functions.revokeAccess(argument).transact()
            receipt = self.w3.eth.waitForTransactionReceipt(hash_tx)

            print(receipt)
        except Exception as e:
            print(e)
            print("[1][Error!]")
