from datetime import datetime
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from click import command
from application import *
from pageOne import *
import DAO


class TransactionPage(tk.Frame):

    replen = 0

    lbl = [['' for _ in range(100)] for _ in range(7)]

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        transactionModeTitlelbl = tk.Label(self, text = "Transaction Mode")
        transactionModeTitlelbl.grid(column = 0, row = 0, columnspan = 12)
        
        dividendModebutton = tk.Button(self, text="Dividend Mode",
                           command=lambda: controller.show_frame("PageOne"))
        dividendModebutton.grid(column=9, row=1)

        newTransactionbutton = tk.Button(self, text="New Transaction",
                           command=lambda: controller.show_frame("NewTransaction"))
        newTransactionbutton.grid(column=8, row=1)

        button = tk.Button(self, text="New Account",
                           command=lambda: controller.show_frame("NewAccount"))
        button.grid(column=7, row=1)

        button = tk.Button(self, text="Generate Report",
                           command=self.genAccTransReportButton)
        button.grid(column=6, row=1)

        button = tk.Button(self, text="Import Transactions",
                           command=self.importTransButton)
        button.grid(column=6, row=2)

        button = tk.Button(self, text="Export Report",
                           command=self.exportReportButton)
        button.grid(column=7, row=2)

        Acclbl = tk.Label(self, text = "Accounts:")
        Acclbl.grid(column=0, row=1)

        self.AccountCombo = ttk.Combobox(self, postcommand = self.updateAcclist)
        self.AccountCombo.grid(column=1, row=1)

        Yearlbl = tk.Label(self, text = "Year:")
        Yearlbl.grid(column=0, row=2)

        self.YearCombo = ttk.Combobox(self, values = [str(i-1) + '-' + str(i)[-2:] for i in range(datetime.now().year+1, 2010, -1)])
        self.YearCombo.grid(column=1, row=2)

        self.canv = tk.Canvas(self, width=800, height=400, bg="red")
        self.canv.grid(column=0, row=5, columnspan=15)

        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canv.yview)
        scrollbar.grid(row=5, column=16, sticky=tk.NS)
        self.canv.configure(yscrollcommand= scrollbar.set)
        self.canv.bind('<Configure>', lambda e : self.canv.configure(scrollregion=self.canv.bbox("all")))
        self.frame = tk.Frame(self.canv, bg="pink")
        self.canv.create_window((0,0), window=self.frame, anchor="nw")
        self.canv.bind_all("<MouseWheel>", self._on_mousewheel)

        self.frame.bind("<Configure>", self.reset_scrollregion)


        lbl = tk.Label(self.frame, text = "Date")
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
        lbl = tk.Label(self.frame, text = "Total Quantity")
        lbl.grid(column=6, row=0)


    def reset_scrollregion(self, event):
        self.canv.configure(scrollregion=self.canv.bbox("all"))

    def _on_mousewheel(self, event):
        self.canv.yview_scroll(int(-1*(event.delta/120)), "units")

    def genAccTransReportButton(self):
        for i in range(self.replen):
            for j in range(7):
                self.lbl[j][i].destroy()

        self.report = genAccTransReport(DAO.getAccount(self.AccountCombo.get()), int("20"+self.YearCombo.get()[-2:]))
        self.replen = len(self.report)
        
        for i in range(len(self.report)):
            self.lbl[0][i] = tk.Label(self.frame, text= self.report[i]['Date'])
            self.lbl[0][i].grid(column=0, row=1+i)
            self.lbl[1][i] = tk.Label(self.frame, text= self.report[i]['ISIN Code'])
            self.lbl[1][i].grid(column=1, row=1+i)
            self.lbl[2][i] = tk.Label(self.frame, text= self.report[i]['Company Name'])
            self.lbl[2][i].grid(column=2, row=1+i)
            self.lbl[3][i] = tk.Label(self.frame, text= self.report[i]['Quantity'])
            self.lbl[3][i].grid(column=3, row=1+i)
            self.lbl[4][i] = tk.Label(self.frame, text= self.report[i]['Unit Price'])
            self.lbl[4][i].grid(column=4, row=1+i)
            self.lbl[5][i] = tk.Label(self.frame, text= self.report[i]['Amount'])
            self.lbl[5][i].grid(column=5, row=1+i)
            self.lbl[6][i] = tk.Label(self.frame, text= self.report[i]['Total Quantity'])
            self.lbl[6][i].grid(column=6, row=1+i)

    def updateAcclist(self):
        acclist = DAO.getAccountList()
        self.AccountCombo['values'] = acclist

    def importTransButton(self):
        filename = fd.askopenfilename()
        DAO.importTransAcc(self.AccountCombo.get(), filename)
        

    def exportReportButton(self):
        rep = pd.DataFrame(self.report)
        rep.to_csv("reports\\TransactionReport"+ self.AccountCombo.get() + str(datetime.now().strftime("%Y%m%d%H%M%S")) + ".csv", sep='\t')
