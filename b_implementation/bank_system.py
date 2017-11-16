from customer import Customer
from admin import Admin
from account import Account


customers_list = []
admins_list = []

	
class BankSystem(object):
    def __init__(self):
        self.customers_list = []
        self.admins_list = []
        self.load_bank_data()


    def load_bank_data(self):
        customer_1 = Customer("Adam", "1234", ["14", "Wilcot Street", "Bath", "B5 5RT"])
        account_no = 1234
        account_1 = Account(5000.00, account_no)
        customer_1.open_account(account_1)
        self.customers_list.append(customer_1)

        customer_2 = Customer("David", "password", ["60", "Holborn Viaduct", "London", "EC1A 2FD"])
        account_no+=1
        account_2 = Account(3200.00,account_no)
        customer_2.open_account(account_2)
        self.customers_list.append(customer_2)


        customer_3 = Customer("Alice", "MoonLight", ["5", "Cardigan Street", "Birmingham", "B4 7BD"])
        account_no+=1
        account_3 = Account(18000.00,account_no)
        customer_3.open_account(account_3)
        self.customers_list.append(customer_3)


        customer_4 = Customer("Ali", "150A",["44", "Churchill Way West", "Basingstoke", "RG21 6YR"])
        account_no+=1
        account_4 = Account(40.00,account_no)
        customer_4.open_account(account_4)
        self.customers_list.append(customer_4)


        admin_1 = Admin("Julian", "1441", True, ["12", "London Road", "Birmingham", "B95 7TT"])
        self.admins_list.append(admin_1)

        admin_2 = Admin("Eva", "2222", False, ["47", "Mars Street", "Newcastle", "NE12 6TZ"])
        self.admins_list.append(admin_2)


    def customer_login(self, name, password):
        #STEP A.1
        pass
        
    def search_customers_by_name(self, customer_name):
        #STEP A.2
        pass


    def main_menu(self):
        #print the options you have
        print()
        print()
        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("Welcome to the Python Bank System")
        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("1) Admin login")
        print ("2) Customer login")
        print ("3) Quit Python Bank System")
        print (" ")
        option = int(input ("Choose your option: "))
        return option

    def run_main_option(self):
        loop = 1         
        while loop == 1:
            choice = self.main_menu()
            if choice == 1:
                name = input ("\nPlease input admin name: ")
                password = input ("\nPlease input admin password: ")
                msg = self.admin_login(name, password)
                print(msg)
            elif choice == 2:
                name = input ("\nPlease input customer name: ")
                password = input ("\nPlease input customer password: ")
                msg = self.customer_login(name, password)
                print(msg)
            elif choice == 3:
                loop = 0
        print ("Thank-You for stopping by the bank!")


    def transferMoney(self, sender_account, receiver_name, receiver_account_no, amount):
        pass

    def customer_menu(self, customer_name):
        #print the options you have
         print (" ")
         print ("Welcome %s : Your transaction options are:" %customer_name)
         print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
         print ("1) Transfer money")
         print ("2) Other account operations")
         print ("3) profile settings")
         print ("4) Sign out")
         print (" ")
         option = int(input ("Choose your option: "))
         return option

    
    def run_customer_options(self, customer):
                    
        account = customer.get_account()            
        loop = 1
        while loop == 1:
            choice = self.customer_menu(customer.get_name())
            if choice == 1:
                pass
            elif choice == 2:
                account.run_account_options()
            elif choice == 3:
                customer.run_profile_options()
            elif choice == 4:
                loop = 0
        print ("Exit account operations")

                
    def admin_login(self, name, password):
        # STEP A.3
        pass


    def search_admin_by_name(self, admin_name):
        # STEP A.4
        pass


    def admin_menu(self, admin_name):
        #print the options you have
         print (" ")
         print ("Welcome Admin %s : Avilable options are:" %admin_name)
         print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
         print ("1) Transfer money")
         print ("2) Customer account operations")
         print ("3) Customer profile settings")
         print ("4) Admin profile settings")
         print ("5) Delete customer")
         print ("6) Print all customers detail")
         print ("7) Sign out")
         print (" ")
         option = int(input ("Choose your option: "))
         return option


    def run_admin_options(self, admin):
                                
        loop = 1
        while loop == 1:
            choice = self.admin_menu(admin.get_name())
            if choice == 1:
                pass
            elif choice == 2:
                #STEP A.5
                pass
            elif choice == 3:
                #STEP A.6
                pass
            elif choice == 4:
                #STEP A.7
                pass
            elif choice == 5:
                #STEP A.8
                pass
            elif choice == 6:
                #STEP A.9
                pass
            elif choice == 7:
                loop = 0
        print ("Exit account operations")


    def print_all_accounts_details(self):
            # list related operation - move to main.py
            i = 0
            for c in self.customers_list:
                i+=1
                print('\n %d. ' %i, end = ' ')
                c.print_details()
                print("------------------------")

        



app = BankSystem()
app.run_main_option()
