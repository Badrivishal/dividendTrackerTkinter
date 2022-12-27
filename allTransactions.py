import tkinter as tk
from tkinter import Toplevel, font as tkfont
from tkinter import messagebox as tkMessageBox
from tkinter import ttk
from application import *
from pageOne import *
from datetime import datetime
import DAO
from tkcalendar import DateEntry


class AllTransactions(tk.Frame):

    replen = 0

    lbl = [['' for i in range(1000)] for i in range(11)]

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.companyList = DAO.getCompanyList()
        lbl = tk.Label(self, text = "All Transactions Mode", font='Helvetica 16 bold')
        lbl.grid(column = 0, row = 0, columnspan = 12)
        
        button = tk.Button(self, text="Transaction Mode",
                           command=lambda: controller.show_frame("TransactionPage"))
        button.grid(column=9, row=1)

        button = tk.Button(self, text="Show Transactions",
                           command=self.genAllTransButton)
        button.grid(column=6, row=1)

        Acclbl = tk.Label(self, text = "Accounts:")
        Acclbl.grid(column=0, row=1)

        self.AccountCombo = ttk.Combobox(self, postcommand = self.updateAcclist)
        self.AccountCombo.grid(column=1, row=1)

        Fromlbl = tk.Label(self, text = "From:")
        Fromlbl.grid(column=0, row=2)

        self.fromDateField=DateEntry(self,selectmode='day',date_pattern='dd-mm-yyyy')        
        self.fromDateField.grid(column=1, row=2)

        Tolbl = tk.Label(self, text = "To:")
        Tolbl.grid(column=2, row=2)

        self.toDateField=DateEntry(self,selectmode='day',date_pattern='dd-mm-yyyy')        
        self.toDateField.grid(column=3, row=2)

        # self.YearCombo = ttk.Combobox(self, values = [str(i-1) + '-' + str(i)[-2:] for i in range(datetime.now().year+1, 2010, -1)])
        # self.YearCombo.grid(column=1, row=2)

        searchLabel = tk.Label(self, text = "Search:")
        searchLabel.grid(column=7, row=2, sticky = tk.E)

        self.searchBox = tk.Entry(self)
        self.searchBox.grid(column=8, row=2)
        self.searchBox.bind('<Return>', self.updateReport)

        self.canv = tk.Canvas(self, width=1500, height=600,  bg="red")
        self.canv.grid(column=0, row=5, columnspan=16)

        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canv.yview)
        scrollbar.grid(row=5, column=17, sticky=tk.NS)
        self.canv.configure(yscrollcommand= scrollbar.set)
        self.canv.bind('<Configure>', lambda e : self.canv.configure(scrollregion=self.canv.bbox("all")))
        self.frame = tk.Frame(self.canv, bg="pink")
        self.canv.create_window((0,0), window=self.frame, anchor="nw")
        self.canv.bind_all("<MouseWheel>", self._on_mousewheel)

        self.frame.bind("<Configure>", self.reset_scrollregion)

        self.canv.bind("<Left>",  lambda event: self.canv.xview_scroll(-1, "units"))
        self.canv.bind("<Right>", lambda event: self.canv.xview_scroll( 1, "units"))
        self.canv.bind("<Up>",    lambda event: self.canv.yview_scroll(-1, "units"))
        self.canv.bind("<Down>",  lambda event: self.canv.yview_scroll( 1, "units"))



        lbl = tk.Label(self.frame, text = "Transaction Date")
        lbl.grid(column=0, row=4)
        lbl = tk.Label(self.frame, text = "ISIN Code")
        lbl.grid(column=1, row=4)
        lbl = tk.Label(self.frame, text = "Company Name")
        lbl.grid(column=2, row=4)
        lbl = tk.Label(self.frame, text = "Transaction Type")
        lbl.grid(column=3, row=4)
        lbl = tk.Label(self.frame, text = "Quantity")
        lbl.grid(column=4, row=4)
        lbl = tk.Label(self.frame, text = "Amount")
        lbl.grid(column=5, row=4)
        # lbl = tk.Label(self.frame, text = "Unit Price")
        # lbl.grid(column=6, row=4)
        # lbl = tk.Label(self.frame, text = "Recieved Amount")
        # lbl.grid(column=7, row=4)
        # lbl = tk.Label(self.frame, text = "Tax Amount")
        # lbl.grid(column=8, row=4)
        # lbl = tk.Label(self.frame, text = "Final Amount")
        # lbl.grid(column=9, row=4)
        # lbl = tk.Label(self.frame, text = "Recv Button")
        # lbl.grid(column=10, row=4)

    def reset_scrollregion(self, event):
        self.canv.configure(scrollregion=self.canv.bbox("all"))

    def _on_mousewheel(self, event):
        self.canv.yview_scroll(int(-1*(event.delta/120)), "units")


    def genAllTransButton(self):
        accountSelected = self.AccountCombo.get()
        fromSelected = self.fromDateField.get_date()
        toSelected = self.toDateField.get_date()
        if not (accountSelected == '' or fromSelected == '' or toSelected == ''):
            account = DAO.getAccount(accountSelected)
            self.globalreport = account
            self.report = self.globalreport
            self.updateTable()
            
            self.canv.focus_set()
        else:
            tkMessageBox.showerror("Error","Please Select Account And Year to generate the Report")

    def updateAcclist(self):
        acclist = DAO.getAccountList()
        self.AccountCombo['values'] = acclist

    def EditTrans(self, val):
        global pop
        pop = Toplevel(self)
        pop.title("Edit Transaction")
        lbl1 = tk.Label(pop, text = "Date")
        lbl1.grid(column=0, row=1)
        # lbl2 = tk.Label(pop, text = "Account")
        # lbl2.grid(column=0, row=2)
        lbl3 = tk.Label(pop, text = "Company")
        lbl3.grid(column=0, row=2)
        lbl4 = tk.Label(pop, text = "Transaction Type")
        lbl4.grid(column=0, row=3)
        lbl5 = tk.Label(pop, text = "Quantity")
        lbl5.grid(column=0, row=4)
        lbl6 = tk.Label(pop, text = "Amount")
        lbl6.grid(column=0, row=5)

        self.dateField=DateEntry(pop,selectmode='day',date_pattern='dd-mm-yyyy')        
        self.dateField.grid(column=1, row=1)
        self.dateField.set_date(datetime.strptime(str(self.report.transactions[val].date), '%Y%m%d'))
        self.CompanyCombo = ttk.Combobox(pop, values = self.companyList, width=50)
        self.CompanyCombo.grid(column=1, row=2)
        self.CompanyCombo.bind('<KeyRelease>', self.companySearch)
        self.CompanyCombo.set(self.report.transactions[val].company.companyName)
        self.TransTypeCombo = ttk.Combobox(pop, values=["Opening Balance", "Purchase", "Sale"])
        self.TransTypeCombo.grid(column=1, row=3)
        self.TransTypeCombo.set(self.report.transactions[val].transType)
        self.quantityField = tk.Entry(pop)
        self.quantityField.grid(column=1, row=4)
        self.quantityField.insert(0, self.report.transactions[val].quantity)
        self.amountField = tk.Entry(pop)
        self.amountField.grid(column=1, row=5)
        self.amountField.insert(0, "{:.2f}".format(self.report.transactions[val].amount))

        button = tk.Button(pop, text="Submit",
                           command=lambda: self.updateRecieved(val, self.dateField.get_date().strftime("%Y%m%d"), self.CompanyCombo.get(), 
                           self.TransTypeCombo.get(), self.quantityField.get(), self.amountField.get()))
        button.grid(column=1, row=6)
        delete = tk.Button(pop, text="Delete", command=lambda:self.deleteTrans(val))
        delete.grid(column=2, row=0)

    def updateTable(self):
        print("hi, updateTable is called")
        for i in range(self.replen):
            for j in range(6):
                self.lbl[j][i].destroy()
        self.replen = len(self.report.transactions)
        
        for i in range(len(self.report.transactions)):
            self.lbl[0][i] = tk.Label(self.frame, text= datetime.strptime(str(self.report.transactions[i].date), '%Y%m%d').strftime("%d/%m/%y"))
            self.lbl[0][i].grid(column=0, row=5+i)
            self.lbl[1][i] = tk.Label(self.frame, text= self.report.transactions[i].company.isinCode)
            self.lbl[1][i].grid(column=1, row=5+i)
            self.lbl[2][i] = tk.Label(self.frame, text= self.report.transactions[i].company.companyName)
            self.lbl[2][i].grid(column=2, row=5+i, sticky = tk.W)
            self.lbl[3][i] = tk.Label(self.frame, text= self.report.transactions[i].transType)
            self.lbl[3][i].grid(column=3, row=5+i, sticky = tk.E)
            self.lbl[4][i] = tk.Label(self.frame, text= self.report.transactions[i].quantity)
            self.lbl[4][i].grid(column=4, row=5+i, sticky = tk.E)
            self.lbl[5][i] = tk.Label(self.frame, text= "{:.2f}".format(self.report.transactions[i].amount))
            self.lbl[5][i].grid(column=5, row=5+i, sticky = tk.E)
            self.lbl[6][i] = tk.Button(self.frame, text="Edit Transactions",
                        command=lambda val=i: self.EditTrans(val))
            self.lbl[6][i].grid(column=10, row=5+i)
        

    def updateReport(self, a):
        # self.globalreport
        txt = self.searchBox.get()
        if txt == '':
            self.report = self.globalreport
        else:    
            self.report = []
            for i in range(len(self.globalreport)):
                for j in self.globalreport[i].values():
                    if txt.lower() in str(j).lower():
                        self.report.append(self.globalreport[i])
                        break
        self.updateTable()
        self.canv.focus_set()

    def deleteTrans(self, uid):
        account = DAO.getAccount(self.AccountCombo.get())
        account.transactions.pop(uid)
        DAO.writeTrans(account)
        self.globalreport = account
        self.report = self.globalreport
        self.updateTable()
        pop.destroy()

    
    def updateRecieved(self, uid, date, companyName, transType, quantity, amount):
        # print(uid, date, amount)
        company = DAO.getCompany(companyName)

        account = DAO.getAccount(self.AccountCombo.get())
        account.transactions[uid].date = date
        account.transactions[uid].company = company
        account.transactions[uid].transType = transType
        account.transactions[uid].quantity = int(quantity)
        account.transactions[uid].amount = float(amount)
        DAO.writeTrans(account)
        # for company in account.companiesInHolding:
        #     for div in company.dividendsDeclared:
        #         if div.uid == uid:
        #             div.update(date, amount)
        # DAO.updateAccountDiv(account.accountHoldersName, account)
        self.lbl[0][uid].destroy()
        self.lbl[1][uid].destroy()
        self.lbl[2][uid].destroy()
        self.lbl[3][uid].destroy()
        self.lbl[4][uid].destroy()
        self.lbl[5][uid].destroy()
        self.lbl[0][uid] = tk.Label(self.frame, text= datetime.strptime(str(date), '%Y%m%d').strftime("%d/%m/%y"))
        self.lbl[0][uid].grid(column=0, row=5+uid)
        self.lbl[1][uid] = tk.Label(self.frame, text= company.isinCode)
        self.lbl[1][uid].grid(column=1, row=5+uid)
        self.lbl[2][uid] = tk.Label(self.frame, text= company.companyName)
        self.lbl[2][uid].grid(column=2, row=5+uid, sticky = tk.W)
        self.lbl[3][uid] = tk.Label(self.frame, text= transType)
        self.lbl[3][uid].grid(column=3, row=5+uid, sticky = tk.E)
        self.lbl[4][uid] = tk.Label(self.frame, text= quantity)
        self.lbl[4][uid].grid(column=4, row=5+uid, sticky = tk.E)
        self.lbl[5][uid] = tk.Label(self.frame, text= "{:.2f}".format(float(amount)))
        self.lbl[5][uid].grid(column=5, row=5+uid, sticky = tk.E)

        self.globalreport.transactions[uid].date = date
        self.globalreport.transactions[uid].company = company
        self.globalreport.transactions[uid].transType = transType
        self.globalreport.transactions[uid].quantity = int(quantity)
        self.globalreport.transactions[uid].amount = float(amount)

        # print(type(self.report[uid]['Recieved Date']), type(self.report[uid]['Recieved Amount']))
        # self.report[uid]['Recieved Date'] = date
        # self.report[uid]['Recieved Amount'] = amount
        # self.total_div_lbl['text'] = "{:.2f}".format(sum([float(i['Dividend Amount']) for i in self.report if len(str(i['Recieved Date']))!=0]))
        # self.total_lbl['text'] = "{:.2f}".format(sum([float(i['Recieved Amount']) for i in self.report if len(str(i['Recieved Amount']))!=0]))
        # self.total_tax_lbl['text'] ="{:.2f}".format(float(self.total_div_lbl['text']) - float(self.total_lbl['text']))
        # self.total_unrecieved_div_lbl['text']="{:.2f}".format(sum([float(i['Dividend Amount']) for i in self.report if len(str(i['Recieved Date']))==0]))

        pop.destroy()


    def exportReportButton(self):
        rep = pd.DataFrame(self.report)
        rep.to_csv("..\\reports\\DividendReport" + self.AccountCombo.get() + str(datetime.now().strftime("%Y%m%d%H%M%S")) + ".csv")

    def companySearch(self, event):
        # pass
        value = event.widget.get()
        if value == '':
            self.CompanyCombo['value'] = self.companyList
        else:
            _hit = []
            for element in self.companyList:
                if value.lower() in element.lower():  # Match case insensitively
                    _hit.append(element)
            self.CompanyCombo['value'] = _hit