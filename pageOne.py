import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from application import *
from pageOne import *
import pickle
import app
import DAO


class PageOne(tk.Frame):

    replen = 0

    lbl = [['' for i in range(100)] for i in range(10)]

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        lbl = tk.Label(self, text = "Dividend Mode")
        lbl.grid(column = 0, row = 0, columnspan = 12)
        
        button = tk.Button(self, text="Transaction Mode",
                           command=lambda: controller.show_frame("TransactionPage"))
        button.grid(column=9, row=1)

        button = tk.Button(self, text="Generate Report",
                           command=self.genAccDivReportButton)
        button.grid(column=6, row=1)

        Acclbl = tk.Label(self, text = "Accounts:")
        Acclbl.grid(column=0, row=1)

        self.AccountCombo = ttk.Combobox(self, postcommand = self.updateAcclist)
        self.AccountCombo.grid(column=1, row=1)

        Yearlbl = tk.Label(self, text = "Year:")
        Yearlbl.grid(column=0, row=2)

        self.YearCombo = ttk.Combobox(self, values = [str(i-1) + '-' + str(i)[-2:] for i in range(2022, 2010, -1)])
        self.YearCombo.grid(column=1, row=2)

        lbl = tk.Label(self, text = "Date")
        lbl.grid(column=0, row=4)
        lbl = tk.Label(self, text = "ISIN Code")
        lbl.grid(column=1, row=4)
        lbl = tk.Label(self, text = "Company Name")
        lbl.grid(column=2, row=4)
        lbl = tk.Label(self, text = "Dividend Declared")
        lbl.grid(column=3, row=4)
        lbl = tk.Label(self, text = "Quantity")
        lbl.grid(column=4, row=4)
        lbl = tk.Label(self, text = "Dividend Amount")
        lbl.grid(column=5, row=4)
        lbl = tk.Label(self, text = "Recieved Date")
        lbl.grid(column=6, row=4)
        lbl = tk.Label(self, text = "Recieved Amount")
        lbl.grid(column=7, row=4)
        lbl = tk.Label(self, text = "Tax Amount")
        lbl.grid(column=8, row=4)
        lbl = tk.Label(self, text = "Final Amount")
        lbl.grid(column=9, row=4)
        # lbl.

        # for i in range(10):
        # if self.AccountCombo.get() in app.database.keys():
        #     report = genAccTransReport(app.database[self.AccountCombo.get()], int(YearCombo.get()[:5]))
        #     print(report)
            # for i in range(len(report)):
            #     lbl = tk.Label(self, text= report[i])

    def genAccDivReportButton(self):

        for i in range(self.replen):
            for j in range(10):
                self.lbl[j][i].destroy()
                # self.lbl.grid(column=j, row=5+i)
        # self.update()
        # self.destroy()
        # self.__init__(parent)
        # print()
        # a = DAO.getAccount(self.AccountCombo.get())
        # print()
        report = genAccDividendReport(DAO.getAccount(self.AccountCombo.get()), int("20"+self.YearCombo.get()[-2:]))
        print(report)
        self.replen = len(report)
        
        for i in range(len(report)):
        # if self.AccountCombo.get() in app.database.keys():
        #     report = genAccTransReport(app.database[self.AccountCombo.get()], int(YearCombo.get()[:5]))
        #     print(report)
            # for i in range(len(report)):
            self.lbl[0][i] = tk.Label(self, text= report[i]['Date'])
            self.lbl[0][i].grid(column=0, row=5+i)
            self.lbl[1][i] = tk.Label(self, text= report[i]['ISIN Code'])
            self.lbl[1][i].grid(column=1, row=5+i)
            self.lbl[2][i] = tk.Label(self, text= report[i]['Company Name'])
            self.lbl[2][i].grid(column=2, row=5+i)
            self.lbl[3][i] = tk.Label(self, text= report[i]['Dividend Declared'])
            self.lbl[3][i].grid(column=3, row=5+i)
            self.lbl[4][i] = tk.Label(self, text= report[i]['Quantity'])
            self.lbl[4][i].grid(column=4, row=5+i)
            self.lbl[5][i] = tk.Label(self, text= report[i]['Dividend Amount'])
            self.lbl[5][i].grid(column=5, row=5+i)
            self.lbl[6][i] = tk.Label(self, text= report[i]['Recieved Date'])
            self.lbl[6][i].grid(column=6, row=5+i)
            self.lbl[7][i] = tk.Label(self, text= report[i]['Recieved Amount'])
            self.lbl[7][i].grid(column=7, row=5+i)
            self.lbl[8][i] = tk.Label(self, text= report[i]['Tax Amount'])
            self.lbl[8][i].grid(column=8, row=5+i)
            self.lbl[9][i] = tk.Label(self, text= report[i]['Final Amount'])
            self.lbl[9][i].grid(column=9, row=5+i)


        
    
    def updateAcclist(self):
        acclist = DAO.getAccountList()
        self.AccountCombo['values'] = acclist


