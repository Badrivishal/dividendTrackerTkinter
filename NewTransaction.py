import tkinter as tk
from tkinter import messagebox as tkMessageBox
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import ttk
from application import *
from pageOne import *
from TransactionPage import *
from tkcalendar import DateEntry



class NewTransaction(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        button = tk.Button(self, text="Back",command=lambda: controller.show_frame("TransactionPage"))
        button.grid(column=0, row=0)

        lbl = tk.Label(self, text = "New Transaction")
        lbl.grid(column = 3, row = 0, columnspan = 12)
        
        lbl1 = tk.Label(self, text = "Date")
        lbl1.grid(column=0, row=1)
        lbl2 = tk.Label(self, text = "Account")
        lbl2.grid(column=0, row=2)
        lbl3 = tk.Label(self, text = "Company")
        lbl3.grid(column=0, row=3)
        lbl4 = tk.Label(self, text = "Transaction Type")
        lbl4.grid(column=0, row=4)
        lbl5 = tk.Label(self, text = "Quantity")
        lbl5.grid(column=0, row=5)
        lbl6 = tk.Label(self, text = "Amount")
        lbl6.grid(column=0, row=6)
        

        self.dateField=DateEntry(self,selectmode='day',date_pattern='dd-mm-yyyy')        
        self.dateField.grid(column=1, row=1)

        self.AccountCombo = ttk.Combobox(self, postcommand = self.updateAcclist)
        self.AccountCombo.grid(column=1, row=2)
        # lbl2.grid(column=1, row=2)
        self.CompanyCombo = AutocompleteCombobox(self, completevalues = DAO.getCompanyList(), width=50)
        self.CompanyCombo.grid(column=1, row=3)
        self.TransTypeCombo = ttk.Combobox(self, values=["Opening Balance", "Purchase", "Sale"])
        self.TransTypeCombo.grid(column=1, row=4)
        self.quantityField = tk.Entry(self)
        self.quantityField.grid(column=1, row=5)
        self.accountField = tk.Entry(self)
        self.accountField.grid(column=1, row=6)
        

        button = tk.Button(self, text="Submit",
                           command=self.createNewTransactionButton)
        button.grid(column=1, row=7)

    def updateAcclist(self):
        acclist = DAO.getAccountList()
        self.AccountCombo['values'] = acclist

    def updateComplist(self):
        complist = DAO.getCompanyList()
        self.CompanyCombo['values'] = complist


    def createNewTransactionButton(self):
        dt = self.dateField.get_date()
        # print()
        DAO.newTransaction(self.AccountCombo.get(), dt.strftime("%Y%m%d"), float(self.accountField.get()), int(self.quantityField.get()), self.TransTypeCombo.get(), self.CompanyCombo.get())
        tkMessageBox.showinfo("Information","New Transaction was Added")
        self.controller.show_frame("TransactionPage")
