from datetime import datetime
import tkinter as tk
from tkinter import messagebox as tkMessageBox
from tkinter import filedialog as fd
from tkinter import ttk
from turtle import bgcolor
from click import command
from application import *
from pageOne import *
import DAO

#TODO https://stackoverflow.com/questions/50422735/tkinter-resize-frame-and-contents-with-main-window

class Holdings(tk.Frame):

    replen = 0
    report = []


    lbl = [['' for _ in range(1000)] for _ in range(8)]

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        transactionModeTitlelbl = tk.Label(self, text = "Holdings Mode",font='Helvetica 16 bold')
        transactionModeTitlelbl.grid(column = 0, row = 0, columnspan = 100)
        
        dividendModebutton = tk.Button(self, text="Dividend Mode",
                           command=lambda: controller.show_frame("PageOne"))
        dividendModebutton.grid(column=9, row=1)

        allTransModebutton = tk.Button(self, text="Transaction Edit Mode",
                           command=lambda: controller.show_frame("AllTransactions"))
        allTransModebutton.grid(column=9, row=2)
        # allTransModebutton["state"] = "disabled"

        newTransactionbutton = tk.Button(self, text="Transaction Mode",
                           command=lambda: controller.show_frame("TransactionPage"))
        newTransactionbutton.grid(column=8, row=1)

        # button = tk.Button(self, text="New Account",
        #                    command=lambda: controller.show_frame("NewAccount"))
        # button.grid(column=7, row=1)

        button = tk.Button(self, text="Generate Report",
                           command=self.genAccTransReportButton)
        button.grid(column=6, row=1)

        # button = tk.Button(self, text="Import Transactions",
        #                    command=self.importTransButton)
        # button.grid(column=6, row=2)

        # button = tk.Button(self, text="Export Report",
        #                    command=self.exportReportButton)
        # button.grid(column=7, row=2)

        # button = tk.Button(self, text="Reset",
        #                    command=self.reset)
        # button.grid(column=8, row=2)

        # button = tk.Button(self, text="Account Transactions Export",
        #                    command=self.accTransExp)
        # button.grid(column=8, row=2)

        Acclbl = tk.Label(self, text = "Accounts:")
        Acclbl.grid(column=0, row=1)

        self.AccountCombo = ttk.Combobox(self, postcommand = self.updateAcclist)
        self.AccountCombo.grid(column=1, row=1)

        self.canv = tk.Canvas(self, width=1500, height=600, bg="red")
        self.canv.grid(column=0, row=5, columnspan=16)

        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canv.yview)
        scrollbar.grid(row=5, column=16, sticky=tk.NS)
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

        lbl = tk.Label(self, text="Total Holding Value")
        lbl.grid(column=0, row=6, columnspan=2)
        self.total_hol_lbl = tk.Label(self, text="{:.2f}".format(sum([float(i['Holding Value']) for i in self.report])))
        self.total_hol_lbl.grid(column=2, row=6, sticky=tk.E)
        
        # self.total_lbl = tk.Label(self, text="{:.2f}".format(sum([float(i['Recieved Amount']) for i in self.report if len(str(i['Recieved Date']))!=0])))
        # self.total_lbl.grid(column=2, row=7, sticky=tk.E)

        # self.total_tax_lbl = tk.Label(self, text="{:.2f}".format(float(self.total_div_lbl['text']) - float(self.total_lbl['text'])))
        # self.total_tax_lbl.grid(column=2, row=8, sticky=tk.E)

        # self.total_unrecieved_div_lbl = tk.Label(self, text="{:.2f}".format(sum([float(i['Final Amount']) for i in self.report if len(str(i['Recieved Date']))==0])))
        # self.total_unrecieved_div_lbl.grid(column=7, row=6, sticky=tk.E)

        
        lbl = tk.Label(self.frame, text = "S No.")
        lbl.grid(column=0, row=0)
        lbl = tk.Label(self.frame, text = "ISIN Code")
        lbl.grid(column=1, row=0)
        lbl = tk.Label(self.frame, text = "Company Name")
        lbl.grid(column=2, row=0)
        lbl = tk.Label(self.frame, text = "Quantity")
        lbl.grid(column=3, row=0)
        lbl = tk.Label(self.frame, text = "Unit Price")
        lbl.grid(column=4, row=0)
        lbl = tk.Label(self.frame, text = "Amount")
        lbl.grid(column=5, row=0)
        lbl = tk.Label(self.frame, text = "Current Value")
        lbl.grid(column=6, row=0)
        lbl = tk.Label(self.frame, text = "Holding Value")
        lbl.grid(column=7, row=0)


    def reset_scrollregion(self, event):
        self.canv.configure(scrollregion=self.canv.bbox("all"))

    def _on_mousewheel(self, event):
        self.canv.yview_scroll(int(-1*(event.delta/120)), "units")

    def genAccTransReportButton(self):
        # print(self.replen)
        # print(len(self.lbl[0]))
        accountSelected = self.AccountCombo.get()
        # yearSelected = self.YearCombo.get()
        if accountSelected != '':
            for i in range(self.replen):
                for j in range(8):
                    self.lbl[j][i].destroy()

            self.report = genAccHoldingsReport(DAO.getAccount(accountSelected))
            self.replen = len(self.report)
            
            for i in range(len(self.report)):
                self.lbl[0][i] = tk.Label(self.frame, text= str(i+1))
                self.lbl[0][i].grid(column=0, row=1+i, sticky = tk.W)

                self.lbl[1][i] = tk.Label(self.frame, text= self.report[i]['ISIN Code'])
                self.lbl[1][i].grid(column=1, row=1+i, sticky = tk.W)
                self.lbl[2][i] = tk.Label(self.frame, text= self.report[i]['Company Name'])
                self.lbl[2][i].grid(column=2, row=1+i, sticky = tk.W)
                self.lbl[3][i] = tk.Label(self.frame, text= self.report[i]['Quantity'])
                self.lbl[3][i].grid(column=3, row=1+i, sticky = tk.E)
                self.lbl[4][i] = tk.Label(self.frame, text= "{:.2f}".format(self.report[i]['Unit Price']))
                self.lbl[4][i].grid(column=4, row=1+i, sticky = tk.E)
                self.lbl[5][i] = tk.Label(self.frame, text= "{:.2f}".format(self.report[i]['Amount']))
                self.lbl[5][i].grid(column=5, row=1+i, sticky = tk.E)
                self.lbl[6][i] = tk.Label(self.frame, text= "{:.2f}".format(self.report[i]['Current Value']))
                self.lbl[6][i].grid(column=6, row=1+i, sticky = tk.E)
                self.lbl[7][i] = tk.Label(self.frame, text= "{:.2f}".format(self.report[i]['Holding Value']))
                self.lbl[7][i].grid(column=7, row=1+i, sticky = tk.E)
                if float(self.report[i]['Current Value'])==0:
                    self.lbl[7][i].config(fg = 'white', bg = 'red')
            self.canv.yview_moveto(0)
            self.canv.focus_set()
            self.total_hol_lbl['text'] = "{:.2f}".format(sum([float(i['Holding Value']) for i in self.report]))

        else:
            tkMessageBox.showerror("Error","Please Select Account And Year to generate the Report")

    def updateAcclist(self):
        acclist = DAO.getAccountList()
        self.AccountCombo['values'] = acclist

    def importTransButton(self):
        accountSelected = self.AccountCombo.get()
        if accountSelected != '':
            filename = fd.askopenfilename()
            failed = DAO.importTransAcc(accountSelected, filename)
            if len(failed) == 0:
                tkMessageBox.showinfo("Information","All the transactions were successfully imported to the account "+ self.AccountCombo.get())
            else:
                tkMessageBox.showinfo("Information","Please check the isin Numbers: " + ", ".join(failed))
        else:
            tkMessageBox.showerror("Error","Please Select Account to which you want to import the transactions to")
    # def reset(self):
        # if(tkMessageBox.askquestion("Reset", "All the Accounts and the Corresponding transactions will be deleted \n\n Are you sure you want to reset?") == "yes"):
            # DAO.reset()
        

    def exportReportButton(self):
        rep = pd.DataFrame(self.report)
        rep.to_csv("..\\reports\\TransactionReport"+ self.AccountCombo.get() + str(datetime.now().strftime("%Y%m%d%H%M%S")) + ".csv")

    def accTransExp(self):
        data = DAO.accountTransactions(self.AccountCombo.get())
        data = [["Date", "Type",	"ISIN",	"Total (qty)",	"Total Amount", "Company Name"]] + [[d.date, d.transType, d.company.isinCode, d.quantity, d.amount, d.company.companyName] for d in data]
        rep = pd.DataFrame(data)
        rep.to_csv("..\\reports\\"+ self.AccountCombo.get() + "AccountTransactions" + str(datetime.now().strftime("%Y%m%d%H%M%S")) + ".csv", header=False, index=False)
