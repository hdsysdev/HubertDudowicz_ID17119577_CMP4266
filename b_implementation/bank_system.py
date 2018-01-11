import tkinter as tk
import csv
import os
import random

from account import Account
from admin import Admin
from customer import Customer
from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta, time

customers_list = []
admins_list = []

current_customer = Customer
class BankSystem(tk.Tk):
    def __init__(self):
        self.load_bank_data()

        tk.Tk.__init__(self)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainMenu, CustomerMenu, AdminMenu):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

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
                    currentAcc = Account(row[7], account_no, row[8], row[9])
                    accounts.append(currentCustomer.open_account(currentAcc))
                    customers_list.append(currentCustomer)
                    currentIndex = currentIndex + 1
                elif row[0] == "Admin":
                    # Combine accounts and customer/admin or open accounts with for loop after readcsv
                    customers.append(Admin(row[1], row[2], True, [row[3], row[4], row[5], row[6]]))
                    currentAdmin = customers[currentIndex]
                    currentAcc = Account(row[7], account_no,  row[8], row[9])
                    admins_list.append(currentAdmin)
                    currentIndex = currentIndex + 1
                # Applying fee if its past loan return date
                if currentAcc.getLoanAmount() != 0 and currentAcc.getReturnDate() > datetime.now():
                    balance = currentAcc.get_balance()
                    currentAcc.set_balance(balance - 50)

    def search_customers_by_name(object, customer_name):
        # STEP A.2
        found_customer = None
        for a in customers_list:
            name = a.get_name()
            if name == customer_name:
                found_customer = a
                break
        if found_customer == None:
            print("\nThe customer %s does not exist! Try again...\n" % customer_name)
        return found_customer

    def search_admin_by_name(object, admin_name):
        # STEP A.4
        found_admin = None
        for a in admins_list:
            name = a.get_name()
            if name == admin_name:
                found_admin = a
                break
        if found_admin == None:
            print("\nThe admin %s does not exist! Try again...\n" % admin_name)
        return found_admin

def saveState():
    allaccs = admins_list+customers_list
    tempFile = "tmp.csv"

    with open(tempFile, "w", newline='') as outfile:
        writeCSV = csv.writer(outfile, delimiter=',')
        for account in allaccs:
            address = account.get_address()
            if type(account) is Admin:
                writeCSV.writerow(
                    ["Admin", account.get_name(), account.get_password(), address[0], address[1], address[2], address[3], 0,
                     0, "01/01/01"])
            elif type(account) is Customer:
                writeCSV.writerow(
                    ["Customer", account.get_name(), account.get_password(), address[0], address[1], address[2],
                     address[3], account.get_account().get_balance(), account.get_account().getLoanAmount(), account.get_account().getReturnDateStr()])
    os.replace(tempFile, "accounts.csv")

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = Label(self, text="Enter Details")
        var = tk.IntVar()
        logintxt = Label(self, text="Login:")
        passtxt = Label(self, text="Password:")
        inputlogin = Entry(self)
        inputpass = Entry(self)
        adminradio = Radiobutton(self, text="Admin", variable=var, value=1)
        userradio = Radiobutton(self, text="Customer", variable=var, value=2)
        adminradio.deselect()
        userradio.deselect()

        def submitfunc():
            if var.get() == 1:
                admin_login(inputlogin.get(), inputpass.get())
            elif var.get() == 2:
                customer_login(inputlogin.get(), inputpass.get())
            else:
                label.config(text="Please Select Account Type")

        submit = Button(self, text="Submit", command=lambda : submitfunc())

        label.grid(row=0, column=0)
        logintxt.grid(row=1, column=0)
        inputlogin.grid(row=1, column=1)
        passtxt.grid(row=2, column=0)
        inputpass.grid(row=2, column=1)
        adminradio.grid(row=3, column=0)
        userradio.grid(row=4, column=0)
        submit.grid(row=3, column=1)

        def customer_login(name, password):
            # STEP A.1
            found_customer = controller.search_customers_by_name(name)
            if found_customer == None:
                label.config(text="User Not Found")
            else:
                if found_customer.check_password(password) == True:
                    global current_customer
                    current_customer = found_customer
                    controller.show_frame(CustomerMenu)
                else:
                    label.config(text="Incorrect Password")

        def admin_login(name, password):
            # STEP A.3
            found_admin = controller.search_admin_by_name(name)
            if found_admin == None:
                label.config(text="User Not Found")
            else:
                if found_admin.check_password(password) == True:
                    controller.show_frame(AdminMenu)
                else:
                    label.config(text="User Not Found")


class AdminMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def transferMoney(toAcc, fromAcc, amount, title):
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
                            writeCSV.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], balance, row[8], row[9]])
                            valid = True
                        else:
                            writeCSV.writerow(row)
                            title.config(text="You don't have the funds required!")
                    elif row[1] == toAcc and valid == True:
                        balance = int(row[7])
                        balance += amount
                        writeCSV.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], balance, row[8], row[9]])
                        title.config(text="Transfer Complete!")
                        valid = False
                    else:
                        writeCSV.writerow(row)
            os.replace(tempFile, "accounts.csv")

        def openTransfer():
            transferWindow = Toplevel(self)
            v=IntVar()
            title = Label(transferWindow,text="Transfer Money")
            fromAccTxt = Label(transferWindow, text="From Account: ")
            toAccTxt = Label(transferWindow, text="To Account: ")
            amountTxt = Label(transferWindow, text="Amount: ")
            fromAccEntry = Entry(transferWindow)
            toAccEntry = Entry(transferWindow)
            amountEntry = Entry(transferWindow, textvariable=v)
            submit = Button(transferWindow, text="Submit",
                            command=lambda: transferMoney(toAccEntry.get(), fromAccEntry.get(), v.get(), title))


            title.grid(row=0, column=0)
            fromAccTxt.grid(row=1, column=0)
            toAccTxt.grid(row=2, column=0)
            amountTxt.grid(row=3, column=0)
            fromAccEntry.grid(row=1, column=1)
            toAccEntry.grid(row=2, column=1)
            amountEntry.grid(row=3, column=1)
            submit.grid(row=4, column=0)

        def logOut():
            saveState()
            controller.show_frame(MainMenu)

        Label(self, text="Admin Menu").grid(row=0, column=0)
        Button(self, text="Transfer money", command=lambda : openTransfer()).grid(row=1, column=0)
        Button(self, text="Customer Account Operations", command=lambda : customeraccop()).grid(row=2, column=0)
        Button(self, text="Customer Profile Settings", command=lambda : customerprofsettings()).grid(row=3, column=0)
        Button(self, text="Admin Profile Settings", command=lambda : adminprofsettings()).grid(row=4, column=0)
        Button(self, text="Delete Customer", command=lambda : removeacc()).grid(row=5, column=0)
        Button(self, text="List All Customers", command=lambda: listcustomers()).grid(row=6, column=0)
        Button(self, text="View Loan Report", command=lambda: choosereportorder()).grid(row=7, column=0)
        Button(self, text="View Pending Loans", command=lambda: viewpendingloans()).grid(row=8, column=0)
        Button(self, text="Save State", command=lambda: saveState()).grid(row=9, column=0)
        Button(self, text="Log Out", command=lambda: logOut()).grid(row=10, column=0)

        def viewpendingloans():
            loanwin = Toplevel(self)
            with open('pending_loans.csv', 'r') as infile, open("temp_pending.csv", "w", newline='') as outfile:
                readCSV = csv.reader(infile, delimiter=',')
                writeCSV = csv.writer(outfile, delimiter=',')
                iterator = 0
                for row in readCSV:
                    if iterator == 0:
                        Label(loanwin, text="Name: " + row[0]).grid(row=1, column=0)
                        Label(loanwin, text="Amount: " + row[1]).grid(row=2, column=0)
                        Button(loanwin, text="Accept", command=lambda : acceptLoan(row[0], row[1], row[2], row)).grid(row=3, column=0)
                        Button(loanwin, text="Decline", command=lambda : declineLoan(row)).grid(row=3, column=1)
                    else:
                        Label(loanwin, text="Name: " + row[0]).grid(row=1+iterator, column=0)
                        Label(loanwin, text="Amount: " + row[1]).grid(row=2+iterator, column=0)
                        Button(loanwin, text="Accept",command=lambda: acceptLoan(row[0], row[1], row[2], row)).grid(row=3+iterator, column=0)
                        Button(loanwin, text="Decline", command=lambda: declineLoan(row)).grid(row=3+iterator, column=1)
                    iterator += 4
            def declineLoan(row):
                with open('pending_loans.csv', 'r') as infile, open("temp_pending.csv", "w", newline='') as outfile:
                    readCSV = csv.reader(infile, delimiter=',')
                    writeCSV = csv.writer(outfile, delimiter=',')

                    for currentRow in readCSV:
                        if currentRow == row:
                            writeCSV.writerow(["", "", ""])
                os.replace("temp_pending.csv", "pending_loans.csv")
                declinewin = Toplevel(self)
                Label(declinewin, text="Loan Declined").grid(row=0, column=0)

            def acceptLoan(name, amount, returndate, row):
                with open('pending_loans.csv', 'r') as infile, open("temp_pending.csv", "w", newline='') as outfile:
                    readCSV = csv.reader(infile, delimiter=',')
                    writeCSV = csv.writer(outfile, delimiter=',')

                    customer = controller.search_customers_by_name(name)
                    account = customer.get_account()
                    balance = account.get_balance()
                    account.set_balance(balance+ float(amount))
                    account.setLoanAmount(float(amount))
                    account.setReturnDate(returndate)

                    for currentRow in readCSV:
                        if currentRow == row:
                            writeCSV.writerow(["", "", ""])
                os.replace("temp_pending.csv", "pending_loans.csv")
                acceptwin = Toplevel(self)
                Label(acceptwin, text="Loan Accepted").grid(row=0, column=0)


        def listcustomers():
            listWin = Toplevel(self)
            for i in customers_list:
                Label(listWin, text="Name: %s" % i.name).pack()
                Label(listWin, text="Address: %s" % i.address[0]).pack()
                Label(listWin, text="%s" % i.address[1]).pack()
                Label(listWin, text="%s" % i.address[2]).pack()
                Label(listWin, text="%s" % i.address[3]).pack()
                ttk.Separator(listWin, orient=HORIZONTAL).pack(fill=X)

        def choosereportorder():
            orderwin = Toplevel(self)
            Button(orderwin, text="Order By Loan Amount", command=lambda : bubblesortloanamount()).pack()
            Button(orderwin, text="Order By Return Date", command=lambda : bubblesortreturndate()).pack()

            def bubblesortloanamount():
                # Bubble Sort
                changed = True
                while changed:
                    changed = False
                    for i in range(len(customers_list) - 1):
                        if float(customers_list[i].get_account().getLoanAmount()) < float(customers_list[i + 1].get_account().getLoanAmount()):
                            customers_list[i], customers_list[i + 1] = customers_list[i + 1], customers_list[i]
                            changed = True
                listloanreport()

            def bubblesortreturndate():
                # Bubble Sort
                changed = True
                while changed:
                    changed = False
                    for i in range(len(customers_list) - 1):
                        if customers_list[i].get_account().getReturnDate() < customers_list[i + 1].get_account().getReturnDate():
                            customers_list[i], customers_list[i + 1] = customers_list[i + 1], customers_list[i]
                            changed = True
                listloanreport()

            def listloanreport():
                listWin = Toplevel(self)

                for i in customers_list:
                    account = i.get_account()
                    Label(listWin, text="Name: %s" % i.name).pack()
                    if float(account.getLoanAmount()) == 0:
                        Label(listWin, text="Loan Amount: 0").pack()
                        Label(listWin, text="Return Date: N/A").pack()
                    else:
                        Label(listWin, text="Loan Amount: %s" % account.getLoanAmount()).pack()
                        Label(listWin, text="Return Date: %s" % account.getReturnDateStr()).pack()
                    ttk.Separator(listWin, orient=HORIZONTAL).pack(fill=X)


        def removeacc():
            removeaccwin = Toplevel(self)
            Label(removeaccwin, text="Remove Account").grid(row=0, column=0)
            Label(removeaccwin, text="Account Name: ").grid(row=1, column=0)
            accNameEntry = Entry(removeaccwin, textvariable=StringVar())
            Button(removeaccwin, text="Submit", command=lambda: findCustomer()).grid(row=1, column=2)
            accNameEntry.grid(row=1, column=1)

            def findCustomer():
                customer_name = accNameEntry.get()
                customer_account = controller.search_customers_by_name(customer_name)
                if customer_account != None:
                    customers_list.remove(customer_account)
                    removeaccwin.destroy()

        def customerprofsettings():
            profsettings = Toplevel(self)
            v = StringVar();
            title = Label(profsettings, text="Profile Operations")
            accName = Label(profsettings, text="Account Name: ")
            accNameEntry = Entry(profsettings, textvariable=v)
            submit = Button(profsettings, text="Submit", command=lambda: findCustomer(profsettings))

            title.grid(row=0, column=0)
            accName.grid(row=1, column=0)
            accNameEntry.grid(row=1, column=1)
            submit.grid(row=1, column=2)

            def findCustomer(window):
                customer_name = v.get()
                customer = controller.search_customers_by_name(customer_name)
                if customer != None:
                    window.destroy()
                    customer.run_profile_options()
                else:
                    title.config(text="Profile Not Found")

        def adminprofsettings():
            profsettings = Toplevel(self)
            v = StringVar();
            title = Label(profsettings, text="Admin Profile Operations")
            accName = Label(profsettings, text="Account Name: ")
            accNameEntry = Entry(profsettings, textvariable=v)
            submit = Button(profsettings, text="Submit", command=lambda: findAdmin(profsettings))

            title.grid(row=0, column=0)
            accName.grid(row=1, column=0)
            accNameEntry.grid(row=1, column=1)
            submit.grid(row=1, column=2)

            def findAdmin(window):
                admin_name = v.get()
                admin = controller.search_admin_by_name(admin_name)
                if admin != None:
                    window.destroy()
                    admin.run_profile_options()
                else:
                    title.config(text="Admin Profile Not Found")

        def customeraccop():
            # STEP A.5
            accountop = Toplevel(self)
            v = StringVar();
            title = Label(accountop, text="Account Operations")
            accName = Label(accountop, text="Account Name: ")
            accNameEntry = Entry(accountop, textvariable=v)
            submit = Button(accountop, text="Submit", command=lambda: findCustomer(accountop))

            title.grid(row=0, column=0)
            accName.grid(row=1, column=0)
            accNameEntry.grid(row=1, column=1)
            submit.grid(row=1, column=2)

            def findCustomer(window):
                customer_name = v.get()
                customer = controller.search_customers_by_name(customer_name)
                account = None
                if customer != None:
                    account = customer.get_account()
                if account != None:
                    window.destroy()
                    account.run_account_options()
                else:
                    title.config(text="Account Not Found")

class CustomerMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Label(self, text="Customer Menu").grid(row=0, column=0)
        Button(self, text="Transfer Money", command=lambda: openTransfer()).grid(row=1, column=0)
        Button(self, text="Other Account Operations", command=lambda: customeraccop()).grid(row=2, column=0)
        Button(self, text="Profile Settings", command=lambda: customerprofoptions()).grid(row=3, column=0)
        Button(self, text="Request Loan", command=lambda: requestLoan()).grid(row=4, column=0)
        Button(self, text="Return Loan", command=lambda: repayLoan()).grid(row=5, column=0)
        Button(self, text="Sign Out", command=lambda: logOut()).grid(row=6, column=0)

        def logOut():
            saveState()
            controller.show_frame(MainMenu)

        def repayLoan():
            balance = current_customer.get_account().get_balance()
            current_customer.get_account().set_balance(balance - float(current_customer.get_account().getLoanAmount()))
            current_customer.get_account().setReturnDate("01/01/18")
            current_customer.get_account().setLoanAmount(0)
            win = Toplevel(self)
            Label(win, text="Loan Repayed").grid(row=0, column=0)
        def requestLoan():
            loanwin = Toplevel(self)
            label = Label(loanwin, text="How much would you like to loan?")
            label.grid(row=0, column=0)
            v= IntVar()
            requestAmount = Entry(loanwin, textvariable=v)
            requestAmount.grid(row=1, column=0)
            Button(loanwin, text="Submit", command=lambda : fillLoan(label)).grid(row=1, column=1)


            balance = current_customer.get_account().get_balance()
            def fillLoan(label):
                amount = int(requestAmount.get())
                rand = random.randint(1, 11)
                if  amount <= 10000 and rand < 3:
                    current_customer.get_account().set_balance(balance + amount)
                    returnDate = datetime.strftime(datetime.now() + timedelta(days=21), "%x")
                    current_customer.get_account().setReturnDate(returnDate)
                    current_customer.get_account().setLoanAmount(amount)
                    label.config(text="Loan Accepted. Loan must be returned by " + str(returnDate))
                else:
                    if random.randint(1, 11) > 4:
                        with open('pending_loans.csv', 'r') as infile, open("temp_pending.csv", "w",newline='') as outfile:
                            readCSV = csv.reader(infile, delimiter=',')
                            writeCSV = csv.writer(outfile, delimiter=',')
                            for row in readCSV:
                                if row[0] not in (None, ""):
                                    writeCSV.writerow(row)
                            writeCSV.writerow([current_customer.get_name(), requestAmount.get(), datetime.strftime(datetime.now() + timedelta(days=21), "%x")])
                            label.config(text="Loan Sent To Admin For Confirmation")
                        os.replace("temp_pending.csv", "pending_loans.csv")
                    else:
                        label.config(text="Loan Not Accepted")

        def customerprofoptions():
            customer_name = current_customer.get_name()
            customer = controller.search_customers_by_name(customer_name)
            if customer != None:
                customer.run_profile_options()

        def customeraccop():
            customer_name = current_customer.get_name()
            customer = controller.search_customers_by_name(customer_name)
            account = None
            if customer != None:
                account = customer.get_account()
            if account != None:
                account.run_account_options()

        def transferMoney(toAcc, fromAcc, amount, title):
            tempFile = "tmp.csv"

            with open('accounts.csv', 'r') as infile, open(tempFile, "w", newline='') as outfile:
                readCSV = csv.reader(infile, delimiter=',')
                writeCSV = csv.writer(outfile, delimiter=',')
                valid = False
                for row in readCSV:
                    if row[1] == fromAcc:
                        balance = float(row[7])
                        if balance >= amount:
                            balance -= amount
                            writeCSV.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], balance, row[8], row[9]])
                            valid = True
                        else:
                            writeCSV.writerow(row)
                            title.config(text="You don't have the funds required!")
                    elif row[1] == toAcc and valid == True:
                        balance = float(row[7])
                        balance += amount
                        writeCSV.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], balance, row[8], row[9]])
                        title.config(text="Transfer Complete!")
                        valid = False
                    else:
                        writeCSV.writerow(row)
            os.replace(tempFile, "accounts.csv")

        def openTransfer():
            transferWindow = Toplevel(self)
            v = IntVar()
            title = Label(transferWindow, text="Transfer Money")
            toAccTxt = Label(transferWindow, text="To Account: ")
            amountTxt = Label(transferWindow, text="Amount: ")
            toAccEntry = Entry(transferWindow)
            amountEntry = Entry(transferWindow, textvariable=v)
            submit = Button(transferWindow, text="Submit",
                            command=lambda: transferMoney(toAccEntry.get(), current_customer.get_name(), v.get(), title))

            title.grid(row=0, column=0)
            toAccTxt.grid(row=2, column=0)
            amountTxt.grid(row=3, column=0)
            toAccEntry.grid(row=2, column=1)
            amountEntry.grid(row=3, column=1)
            submit.grid(row=4, column=0)

app = BankSystem()
app.mainloop()
