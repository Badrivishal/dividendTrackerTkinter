import tkinter as tk
from tkinter import Toplevel, font as tkfont
from tkinter import messagebox as tkMessageBox
from tkinter import ttk
from application import *
from pageOne import *
from datetime import datetime
import DAO
from tkcalendar import DateEntry


class PageOne(tk.Frame):

    replen = 0

    lbl = [['' for i in range(1000)] for i in range(11)]

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        lbl = tk.Label(self, text = "Dividend Mode", font='Helvetica 16 bold')
        lbl.grid(column = 0, row = 0, columnspan = 12)
        
        button = tk.Button(self, text="Transaction Mode",
                           command=lambda: controller.show_frame("TransactionPage"))
        button.grid(column=9, row=1)

        button = tk.Button(self, text="Generate Report",
                           command=self.genAccDivReportButton)
        button.grid(column=6, row=1)

        button = tk.Button(self, text="Export Report",
                           command=self.exportReportButton)
        button.grid(column=7, row=1)

        Acclbl = tk.Label(self, text = "Accounts:")
        Acclbl.grid(column=0, row=1)

        self.AccountCombo = ttk.Combobox(self, postcommand = self.updateAcclist)
        self.AccountCombo.grid(column=1, row=1)

        Yearlbl = tk.Label(self, text = "Year:")
        Yearlbl.grid(column=0, row=2)

        self.YearCombo = ttk.Combobox(self, values = [str(i-1) + '-' + str(i)[-2:] for i in range(datetime.now().year+1, 2010, -1)])
        self.YearCombo.grid(column=1, row=2)

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



        lbl = tk.Label(self.frame, text = "Date")
        lbl.grid(column=0, row=4)
        lbl = tk.Label(self.frame, text = "ISIN Code")
        lbl.grid(column=1, row=4)
        lbl = tk.Label(self.frame, text = "Company Name")
        lbl.grid(column=2, row=4)
        lbl = tk.Label(self.frame, text = "Dividend Declared")
        lbl.grid(column=3, row=4)
        lbl = tk.Label(self.frame, text = "Quantity")
        lbl.grid(column=4, row=4)
        lbl = tk.Label(self.frame, text = "Dividend Amount")
        lbl.grid(column=5, row=4)
        lbl = tk.Label(self.frame, text = "Recieved Date")
        lbl.grid(column=6, row=4)
        lbl = tk.Label(self.frame, text = "Recieved Amount")
        lbl.grid(column=7, row=4)
        lbl = tk.Label(self.frame, text = "Tax Amount")
        lbl.grid(column=8, row=4)
        lbl = tk.Label(self.frame, text = "Final Amount")
        lbl.grid(column=9, row=4)
        lbl = tk.Label(self.frame, text = "Recv Button")
        lbl.grid(column=10, row=4)

    def reset_scrollregion(self, event):
        self.canv.configure(scrollregion=self.canv.bbox("all"))

    def _on_mousewheel(self, event):
        self.canv.yview_scroll(int(-1*(event.delta/120)), "units")


    def genAccDivReportButton(self):
        accountSelected = self.AccountCombo.get()
        yearSelected = self.YearCombo.get()
        if accountSelected != '' or yearSelected != '':
            for i in range(self.replen):
                for j in range(11):
                    self.lbl[j][i].destroy()
            
            account = DAO.getAccount(accountSelected)
            finYear = int("20"+yearSelected[-2:])
            # account = importDividends(account, finYear)
            
            if datetime.now().month < 4:
                year = datetime.now().year
            else:
                year = datetime.now().year+1

            if finYear != year:
                account = importDividends(account, finYear)
                DAO.updateAccountDiv(accountSelected,  account)


            # print("Updating------------------")
            
            # DAO.updateAccountDiv(accountSelected,  account)
            # print("Updatedddddddd===============================")
            self.report = genAccDividendReport(account, finYear)
            self.replen = len(self.report)
            
            for i in range(len(self.report)):
                self.lbl[0][i] = tk.Label(self.frame, text= datetime.strptime(str(self.report[i]['Date']), '%Y%m%d').strftime("%d/%m/%y"))
                self.lbl[0][i].grid(column=0, row=5+i)
                self.lbl[1][i] = tk.Label(self.frame, text= self.report[i]['ISIN Code'])
                self.lbl[1][i].grid(column=1, row=5+i)
                self.lbl[2][i] = tk.Label(self.frame, text= self.report[i]['Company Name'])
                self.lbl[2][i].grid(column=2, row=5+i, sticky = tk.W)
                self.lbl[3][i] = tk.Label(self.frame, text= "{:.2f}".format(self.report[i]['Dividend Declared']))
                self.lbl[3][i].grid(column=3, row=5+i, sticky = tk.E)
                self.lbl[4][i] = tk.Label(self.frame, text= self.report[i]['Quantity'])
                self.lbl[4][i].grid(column=4, row=5+i, sticky = tk.E)
                self.lbl[5][i] = tk.Label(self.frame, text= "{:.2f}".format(self.report[i]['Dividend Amount']))
                self.lbl[5][i].grid(column=5, row=5+i, sticky = tk.E)
                self.lbl[6][i] = tk.Label(self.frame, text= datetime.strptime(str(self.report[i]['Recieved Date']), '%Y%m%d').strftime("%d/%m/%y") if len(str(self.report[i]['Recieved Date'])) > 1 else "")
                self.lbl[6][i].grid(column=6, row=5+i)
                self.lbl[7][i] = tk.Label(self.frame, text= "{:.2f}".format(float(self.report[i]['Recieved Amount'])))
                self.lbl[7][i].grid(column=7, row=5+i, sticky = tk.E)
                self.lbl[8][i] = tk.Label(self.frame, text= "{:.2f}".format(self.report[i]['Tax Amount']))
                self.lbl[8][i].grid(column=8, row=5+i, sticky = tk.E)
                self.lbl[9][i] = tk.Label(self.frame, text= "{:.2f}".format(self.report[i]['Final Amount']))
                self.lbl[9][i].grid(column=9, row=5+i, sticky = tk.E)
                self.lbl[10][i] = tk.Button(self.frame, text="Add Recieved Note",
                            command=lambda val=i: self.AddRecievedNote(val))
                self.lbl[10][i].grid(column=10, row=5+i)
            # print([i['Recieved Amount'] for i in self.report if len(str(i['Recieved Amount']))!=0])
            lbl = tk.Label(self, text="Total Dividend Amount Declared(In terms of Recieved): ")
            lbl.grid(column=0, row=6, columnspan=2)
            self.total_div_lbl = tk.Label(self, text="{:.2f}".format(sum([float(i['Dividend Amount']) for i in self.report if len(str(i['Recieved Date']))!=0])))
            self.total_div_lbl.grid(column=2, row=6, sticky=tk.E)
            
            lbl = tk.Label(self, text="Total Recieved Amount: ")
            lbl.grid(column=0, row=7, columnspan=2)
            self.total_lbl = tk.Label(self, text="{:.2f}".format(sum([float(i['Recieved Amount']) for i in self.report if len(str(i['Recieved Date']))!=0])))
            self.total_lbl.grid(column=2, row=7, sticky=tk.E)
            
            lbl = tk.Label(self, text="Total Tax Amount Paid(In terms of Recieved): ")
            lbl.grid(column=0, row=8, columnspan=2)
            self.total_tax_lbl = tk.Label(self, text="{:.2f}".format(float(self.total_div_lbl['text']) - float(self.total_lbl['text'])))
            self.total_tax_lbl.grid(column=2, row=8, sticky=tk.E)

            lbl = tk.Label(self, text="Total Amount to be recieved")
            lbl.grid(column=5, row=6, columnspan=2)
            self.total_unrecieved_div_lbl = tk.Label(self, text="{:.2f}".format(sum([float(i['Final Amount']) for i in self.report if len(str(i['Recieved Date']))==0])))
            self.total_unrecieved_div_lbl.grid(column=7, row=6, sticky=tk.E)
            
            self.canv.focus_set()
        else:
            tkMessageBox.showerror("Error","Please Select Account And Year to generate the Report")

    def updateAcclist(self):
        acclist = DAO.getAccountList()
        self.AccountCombo['values'] = acclist

    def AddRecievedNote(self, val):
        global pop
        pop = Toplevel(self)
        pop.title("Update Recieved")
        lab = tk.Label(pop, text= self.report[val]['Company Name'])
        lab.grid(row=0, column=0)
        lab = tk.Label(pop, text= "Recieved Date")
        lab.grid(row=1, column=0)
        lab = tk.Label(pop, text= "Recieved Amount")
        lab.grid(row=2, column=0)
        dateField=DateEntry(pop,selectmode='day',date_pattern='dd-mm-yyyy')        

        dateField.grid(column=1, row=1)
        amountField = tk.Entry(pop)
        amountField.insert(0, "{:.2f}".format(self.report[val]['Final Amount']))
        amountField.grid(column=1, row=2)
        button = tk.Button(pop, text="Submit",
                           command=lambda: self.updateRecieved(self.report[val]['Id'], dateField.get_date().strftime("%Y%m%d"), amountField.get(), val))
        button.grid(column=1, row=3)

        
        
    
    def updateRecieved(self, uid, date, amount, row):
        # print(uid, date, amount)

        account = DAO.getAccount(self.AccountCombo.get())
        for company in account.companiesInHolding:
            for div in company.dividendsDeclared:
                if div.uid == uid:
                    div.update(date, amount)
        DAO.updateAccountDiv(account.accountHoldersName, account)
        self.lbl[6][row].destroy()
        self.lbl[7][row].destroy()
        self.lbl[6][row] = tk.Label(self.frame, text= datetime.strptime(str(date), '%Y%m%d').strftime("%d/%m/%y"))
        self.lbl[6][row].grid(column=6, row=5+row)
        self.lbl[7][row] = tk.Label(self.frame, text= "{:.2f}".format(float(amount)))
        self.lbl[7][row].grid(column=7, row=5+row, sticky = tk.E)
        # print(type(self.report[row]['Recieved Date']), type(self.report[row]['Recieved Amount']))
        self.report[row]['Recieved Date'] = date
        self.report[row]['Recieved Amount'] = amount
        self.total_div_lbl['text'] = "{:.2f}".format(sum([float(i['Dividend Amount']) for i in self.report if len(str(i['Recieved Date']))!=0]))
        self.total_lbl['text'] = "{:.2f}".format(sum([float(i['Recieved Amount']) for i in self.report if len(str(i['Recieved Amount']))!=0]))
        self.total_tax_lbl['text'] ="{:.2f}".format(float(self.total_div_lbl['text']) - float(self.total_lbl['text']))
        self.total_unrecieved_div_lbl['text']="{:.2f}".format(sum([float(i['Dividend Amount']) for i in self.report if len(str(i['Recieved Date']))==0]))

        pop.destroy()


    def exportReportButton(self):
        rep = pd.DataFrame(self.report)
        rep.to_csv("..\\reports\\DividendReport" + self.AccountCombo.get() + str(datetime.now().strftime("%Y%m%d%H%M%S")) + ".csv")
