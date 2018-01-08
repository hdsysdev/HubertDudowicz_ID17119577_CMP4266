import tkinter as tk
from tkinter import *

class Person(object):

    def __init__(self, name, password, address = [None, None, None, None]):
        self.name = name
        self.password = password
        self.address = address
        
    def get_address(self):
        return self.address

    def get_name(self):
        return self.name

    def get_password(self):
        return  self.password

    def check_password(self, password):
        if self.password == password:
            return True
        return False

    def run_profile_options(self):
        window = tk.Tk()

        def update_name():
            nameWin = Toplevel(window)
            v = StringVar()
            Label(nameWin, text="Enter New Name").grid(row=0, column=0)
            nameEntry = Entry(nameWin, textvariable=v)
            nameEntry.grid(row=0, column=1)
            Button(nameWin, text="Submit", command=lambda : setName()).grid(row=0, column=2)

            def setName():
                self.name = nameEntry.get()
                nameWin.destroy()

        def print_details():
            detailsWin = Toplevel(window)
            Label(detailsWin, text="Name: %s" % self.name).grid(row=0, column=0)
            Label(detailsWin, text="Address: %s" % self.address[0]).grid(row=1, column=0)
            Label(detailsWin, text="         %s" % self.address[1]).grid(row=2, column=0)
            Label(detailsWin, text="         %s" % self.address[2]).grid(row=3, column=0)
            Label(detailsWin, text="         %s" % self.address[3]).grid(row=4, column=0)


        def update_address():
            addressWin = Toplevel(window)

            Label(addressWin, text="Enter New Address").grid(row=0, column=0)
            adrln1 = Entry(addressWin, textvariable=StringVar())
            adrln2 = Entry(addressWin, textvariable=StringVar())
            adrln3 = Entry(addressWin, textvariable=StringVar())
            adrln4 = Entry(addressWin, textvariable=StringVar())
            submit = Button(addressWin, text="Submit", command=lambda :setAddress())
            adrln1.grid(row=1, column=0)
            adrln2.grid(row=2, column=0)
            adrln3.grid(row=3, column=0)
            adrln4.grid(row=4, column=0)
            submit.grid(row=5, column=0)

            def setAddress():
                self.address[0] = adrln1.get()
                self.address[1] = adrln2.get()
                self.address[2] = adrln3.get()
                self.address[3] = adrln4.get()
                addressWin.destroy()

        label = Label(window, text="Your Profile Options Are")
        nameButton = Button(window, text="Update Name", command=lambda :update_name())
        detailsButton = Button(window, text="Print Account Details", command=lambda: print_details())
        addressButton = Button(window, text="Update Address", command=lambda :update_address())

        label.grid(row=0, column=0)
        nameButton.grid(row=1, column=0)
        detailsButton.grid(row=2, column=0)
        addressButton.grid(row=3, column=0)
        window.mainloop()