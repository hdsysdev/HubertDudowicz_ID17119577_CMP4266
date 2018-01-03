import tkinter
import csv
import os
import random
import datetime

from account import Account
from admin import Admin
from customer import Customer
from tkinter import *
from datetime import datetime, timedelta

customers_list = []
admins_list = []


class BankSystem(object):
    def __init__(self):
        self.customers_list = []
        self.admins_list = []
        self.load_bank_data()
        self.mw = tkinter.Tk()


    def load_bank_data(self):
        account_no = 1234
        with open('accounts.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            customers = []
            accounts = []
            currentIndex = 0
            for row in readCSV:
                if row[0] == "Customer":
                    customers.append(Customer(row[1], row[2], [row[3], row[4], row[5], row[6]]))
                    currentCustomer = customers[currentIndex]
                    currentAcc = Account(row[7], account_no)
                    accounts.append(currentCustomer.open_account(currentAcc))
                    self.customers_list.append(currentCustomer)
                    currentIndex = currentIndex + 1
                elif row[0] == "Admin":
                    #Combine accouts and customer/admin or open accounts with for loop after readcsv
                    customers.append(Admin(row[1], row[2], True, [row[3], row[4], row[5], row[6]]))
                    currentAdmin = customers[currentIndex]
                    currentAcc = Account(row[7], account_no)
                    self.admins_list.append(currentAdmin)
                    currentIndex = currentIndex + 1
                #Applying fee if its past loan return date
                if currentAcc.getLoanAmount() != 0 and currentAcc.getReturnDate() > datetime.now():
                    balance = currentAcc.get_balance()
                    currentAcc.set_balance(balance - 50)

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
        

    def customer_menu(self, customer_name):
        #print the options you have
         print (" ")
         print ("Welcome %s : Your transaction options are:" %customer_name)
         print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
         print ("1) Transfer money")
         print ("2) Other account operations")
         print ("3) profile settings")
         print("4) Request Loan")
         print("5) Return Loan")
         print ("6) Sign out")
         print (" ")
         option = int(input ("Choose your option: "))
         return option

    def transferMoney(self, fromAcc, toAcc, amount):
        tempFile = "tmp.csv"
        with open('accounts.csv', 'r') as infile, open(tempFile, "w", newline='') as outfile:
            readCSV = csv.reader(infile, delimiter=',')
            writeCSV = csv.writer(outfile, delimiter=',')
            valid = False
            for row in readCSV:
                if row[1] == fromAcc:
                    balance = int(row[7])
                    if balance >= amount:
                        balance -= amount
                        writeCSV.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], balance])
                        valid = True
                    else:
                        print("You do not have the funds required")
                elif row[1] == toAcc and valid == True:
                    balance = int(row[7])
                    balance += amount
                    writeCSV.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], balance])
                else:
                    writeCSV.writerow(row)
        os.replace(tempFile, "accounts.csv")
    
    def run_customer_options(self, customer):
                    
        account = customer.get_account()            
        loop = 1
        while loop == 1:
            choice = self.customer_menu(customer.get_name())
            if choice == 1:
                toAcc = input("Enter name of recipient: ")
                amount = int(input("Enter amount: "))
                self.transferMoney(customer.get_name(), toAcc, amount)
            elif choice == 2:
                account.run_account_options()
            elif choice == 3:
                customer.run_profile_options()
            elif choice ==4:
                requestAmount = int(input("How much would you like to loan: "))
                rand = random.randint(1, 11)
                balance = customer.get_account().get_balance()
                #implement backend storage and add     and rand <  3
                if requestAmount <= 10000 :
                    print("Loan Accepted")
                    customer.get_account().set_balance(balance+requestAmount)
                    returnDate = datetime.now() + timedelta(days=21)
                    customer.get_account().setReturnDate(returnDate)
                    customer.get_account().setLoanAmount(requestAmount)
                    print("Loan must be returned by " + str(returnDate))
                else:
                    print("Loan Not Accepted")
                    
            elif choice == 5:
                balance = customer.get_account().get_balance()
                loanAmount = customer.get_account().getLoanAmount()
                if balance >= loanAmount:
                    customer.get_account().set_balance(balance - loanAmount)
                    print("Loan Cleared")
                    customer.get_account().setReturnDate(0)
                    customer.get_account().setLoanAmount(0)
                else:
                    print("You have insufficient funds")
            elif choice == 6:
                loop = 0
        print ("Exit account operations")


    def admin_menu(self, admin_name):
        #print the options you have
         print (" ")
         print ("Welcome Admin %s : Available options are:" %admin_name)
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