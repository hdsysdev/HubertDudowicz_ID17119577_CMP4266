import tkinter

from account import Account
from admin import Admin
from customer import Customer
from tkinter import *

customers_list = []
admins_list = []


class BankSystem(object):
    def __init__(self):
        self.customers_list = []
        self.admins_list = []
        self.load_bank_data()
        self.mw = tkinter.Tk()


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

        admin_2 = Admin("Jeff", "1234", True, ["47", "Mars Street", "Newcastle", "NE12 6TZ"])
        self.admins_list.append(admin_2)


    def customer_login(self, name, password):
        #STEP A.1
        found_customer = self.search_customers_by_name(name)
        if found_customer == None:
            return "The customer has not been found!\n"
        else:
            if found_customer.check_password(password) == True:
                self.run_customer_options(found_customer)
            else:
                return "you have input a wrong password"
        
    def search_customers_by_name(self, customer_name):
        #STEP A.2
        found_customer = None
        for a in self.customers_list:
            name = a.get_name()
            if name == customer_name:
                found_customer = a
                break
        if found_customer == None:
            print("\nThe customer %s does not exist! Try again...\n" % customer_name)
        return found_customer

    def admin_login(self, name, password):
        # STEP A.3
        found_admin = self.search_admin_by_name(name)
        if found_admin == None:
            return "\n The admin has not been found!\n"
        else:
            if (found_admin.check_password(password) == True):
                self.run_admin_options(found_admin)
            else:
                return "you have input a wrong password"

    def search_admin_by_name(self, admin_name):
        # STEP A.4
        found_admin = None
        for a in self.admins_list:
            name = a.get_name()
            if name == admin_name:
                found_admin = a
                break
        if found_admin == None:
            print("\nThe admin %s does not exist! Try again...\n" % admin_name)
        return found_admin

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
                customer_name = input("\nPlease input customer name :\n")
                customer = self.search_customers_by_name(customer_name)
                if customer != None:
                    account = customer.get_account()
                if account != None:
                    account.run_account_options()
            elif choice == 3:
                #STEP A.6
                customer_name = input("\nPlease input customer name :\n")
                customer = self.search_customers_by_name(customer_name)
                if customer != None:
                    customer.run_profile_options()
            elif choice == 4:
                #STEP A.7
                admin.run_profile_options()
            elif choice == 5:
                if admin.has_full_admin_right() == True:
                    customer_name = input("\nPlease input customer name you want to delete:\n")
                    customer_account = self.search_customers_by_name(customer_name)
                    if customer_account != None:
                        self.customers_list.remove(customer_account)
                    else:
                        print("\nOnly administrators with full admin rights can remove a customer from the bank system!\n")
            elif choice == 6:
                #STEP A.9
                self.print_all_accounts_details()
            elif choice == 7:
                loop = 0
        print ("Exit account operations")


    def print_all_accounts_details(self):
            # list related operation - move to main.py
            i = 0
            for c in self.customers_list:
                i+=1
                print('/n %d. ' %i, end=' ')
                c.print_details()
                print("------------------------")

app = BankSystem()
app.run_main_option()