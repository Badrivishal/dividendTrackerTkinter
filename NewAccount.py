import tkinter as tk
from tkinter import messagebox as tkMessageBox
from application import *
from pageOne import *
from TransactionPage import *
import DAO

class NewAccount(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        backButton = tk.Button(self, text="Back",command=lambda: controller.show_frame("TransactionPage"))
        backButton.grid(column=0, row=0)

        newAccountTitlelbl = tk.Label(self, text = "New Account")
        newAccountTitlelbl.grid(column = 1, row = 0, columnspan = 12)
        
        accNameFormlbl = tk.Label(self, text = "Account Name")
        accNameFormlbl.grid(column=0, row=1)
        
        self.accountNameEntryBox = tk.Entry(self)
        self.accountNameEntryBox.grid(column=1, row=1)

        submitButton = tk.Button(self, text="Submit",
                           command=self.createNewAccountButton)
        submitButton.grid(column=0, row=2)

    def createNewAccountButton(self):
        DAO.newAccount(self.accountNameEntryBox.get())
        self.accountNameEntryBox.delete(0, 'end')
        tkMessageBox.showinfo("Information","New Transaction was Added")

        self.controller.show_frame("TransactionPage")
