import tkinter as tk
from tkinter import font as tkfont
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import ttk
from application import *
from pageOne import *
from TransactionPage import *
import pickle
import app
from tkcalendar import Calendar, DateEntry



class NewTransaction(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        button = tk.Button(self, text="Back",command=lambda: controller.show_frame("TransactionPage"))
        button.grid(column=0, row=0)

        lbl = tk.Label(self, text = "New Transaction")
        lbl.grid(column = 1, row = 0, columnspan = 12)
        
        lbl1 = tk.Label(self, text = "Date")
        lbl1.grid(column=0, row=1)
        lbl2 = tk.Label(self, text = "Account")
        lbl2.grid(column=0, row=2)
        lbl3 = tk.Label(self, text = "Amount")
        lbl3.grid(column=0, row=3)
        lbl4 = tk.Label(self, text = "Quantity")
        lbl4.grid(column=0, row=4)
        lbl5 = tk.Label(self, text = "Company")
        lbl5.grid(column=0, row=5)

        self.dateField=DateEntry(self,selectmode='day',date_pattern='dd-mm-yyyy')        
        self.dateField.grid(column=1, row=1)

        self.AccountCombo = ttk.Combobox(self, postcommand = self.updateAcclist)
        self.AccountCombo.grid(column=1, row=2)
        # lbl2.grid(column=1, row=2)
        self.accountField = tk.Entry(self)
        self.accountField.grid(column=1, row=3)
        self.quantityField = tk.Entry(self)
        self.quantityField.grid(column=1, row=4)
        self.CompanyCombo = AutocompleteCombobox(self, completevalues = DAO.getCompanyList())
        self.CompanyCombo.grid(column=1, row=5)

        button = tk.Button(self, text="Submit",
                           command=self.createNewTransactionButton)
        button.grid(column=0, row=6)

    def updateAcclist(self):
        acclist = DAO.getAccountList()
        self.AccountCombo['values'] = acclist

    def updateComplist(self):
        complist = DAO.getCompanyList()
        self.CompanyCombo['values'] = complist


    def createNewTransactionButton(self):
        dt = self.dateField.get_date()
        # print()
        DAO.newTransaction(self.AccountCombo.get(), dt.strftime("%Y%m%d"), float(self.accountField.get()), int(self.quantityField.get()), "Purchase", self.CompanyCombo.get())

        self.controller.show_frame("StartPage")
