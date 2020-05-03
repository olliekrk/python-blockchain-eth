from datetime import datetime

to_hour_precision = lambda t: datetime.fromtimestamp(t).replace(microsecond=0, second=0, minute=0)

class AppointmentBookingContract:
    
    def __init__(self, contract, w3):
        self.contract = contract
        self.w3 = w3

    def add_appointment(self, name, timestamp, price):
        try:
            date = datetime.timestamp(to_hour_precision(timestamp))
            hash_tx = self.contract.functions.createAppointment(name, int(date), price).transact()
            self.w3.eth.waitForTransactionReceipt(hash_tx)
        except Exception as e:
            print(e)
            print("[1][Error!]")

    def book_appointment(self, timestamp, price, account):
        try:
            date = datetime.timestamp(to_hour_precision(timestamp))
            self.contract.functions.bookAppointment(date).transact({
                'from': account,
                'value': self.web3.toWei(price, 'ether')
            })
        except Exception as e:
            print(e)
            print("[1][Error!]")

    def print_appointments(self):
        r = self.contract.functions.printAppointments().call()
        print(r)


class HealthDataAccessContract:
    
    def __init__(self, contract, w3):
        self.contract = contract
        self.w3 = w3

    def add_heartrate(self, heartrate, date):
        try:
            hash_tx = self.contract.functions.addMeasurement(int(heartrate), int(date)).transact()
            self.w3.eth.waitForTransactionReceipt(hash_tx)
        except Exception as e:
            print(e)
            print("[1][Error!]")

    def get_data(self):
        try:
            r = self.contract.functions.getMeasurements().call()
            print(r)
        except Exception as e:
            print(e)
            print("[1][Error!]")

    def get_last_data(self):
        try:
            r = self.contract.functions.getLastMeasurement().call()
            print(r)
        except Exception as e:
            print(e)
            print("[1][Error!]")

    def grant_access(self, argument):
        try:
            hash_tx = self.contract.functions.grantAccess(argument).transact()
            self.w3.eth.waitForTransactionReceipt(hash_tx)
        except Exception as e:
            print(e)
            print("[1][Error!]")

    def revoke_access(self, argument):
        try:
            hash_tx = self.contract.functions.revokeAccess(argument).transact()
            self.w3.eth.waitForTransactionReceipt(hash_tx)
        except Exception as e:
            print(e)
            print("[1][Error!]")
