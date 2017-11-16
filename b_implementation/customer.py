from person import Person

class Customer(Person):

    def __init__(self, name, password, address = [None, None, None, None]):
        super().__init__(name, password, address)

    def open_account(self, account):
        self.account = account

    def get_account(self):
        return self.account
                            
    def print_details(self):
        super().print_details()
        bal = self.account.get_balance()
        print('Account balance: %.2f' %bal)
        print(" ")

							


