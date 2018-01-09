from datetime import datetime, timedelta
import tkinter as tk
from tkinter import *

class Account:

        def __init__(self, balance, account_no, loanAmount, returnDate):
                self.balance = float(balance)
                self.account_no = account_no
                self.loanAmount = loanAmount
                self.returnDate = datetime.strptime(returnDate, '%m/%d/%y')


        def get_balance(self):
                return self.balance
        
        def set_balance(self, new):
                self.balance = new

        def get_account_no(self):
                return self.account_no
        
        def getLoanAmount(self):
                return self.loanAmount
        
        def setLoanAmount(self, loanAmount):
                self.loanAmount = loanAmount

        def getReturnDate(self):
            # datetime.strptime(, '%m/%d/%y')
                return self.returnDate

        def getReturnDateStr(self):
            # datetime.strptime(self.returnDate, '%m/%d/%y')
                return datetime.strftime(self.returnDate, "%x")

        def setReturnDate(self, returnDate):
                self.returnDate = datetime.strptime(returnDate, '%m/%d/%y')


        def run_account_options(self):
            window = tk.Tk()

            def deposit_money():
                inputWin = Toplevel()
                v = IntVar()
                inputLabel = Label(inputWin, text="Deposit Amount: ")
                inputEntry = Entry(inputWin, textvariable=v)
                inputButton = Button(inputWin, text="Submit", command=lambda: submit())

                inputLabel.grid(row=0, column=0)
                inputEntry.grid(row=0, column=1)
                inputButton.grid(row=0, column=2)
                def submit():
                    inputWin.destroy()
                    self.balance += v.get()

            def checkbalance():
                balanceWin = Toplevel()
                balanceLabel = Label(balanceWin, text="Your Balance Is: ")
                balanceAmount = Label(balanceWin, text=self.get_balance())
                balanceLabel.grid(row=0, column=0)
                balanceAmount.grid(row=0, column=1)

            label = Label(window, text="Your Transaction Options Are: ")
            deposit = Button(window, text="Deposit Money", command=lambda : deposit_money())
            checkBalance = Button(window, text="Check Balance", command=lambda : checkbalance())

            label.grid(row=0, column=0)
            deposit.grid(row=1, column=0)
            checkBalance.grid(row=2, column=0)

            window.mainloop()