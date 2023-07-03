import tkinter as tk
from datetime import date
from tkinter import font as tkfont
from NewAccount import *
from application import *
from pageOne import *
from TransactionPage import *
from NewTransaction import *
from allTransactions import *
from holdings import *


class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Dividend Tracker")
        self.iconbitmap("AppIcon.ico")
        # self.attributes('-fullscreen',True)

        self.title_font = tkfont.Font(family='Helvetica', size=25, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (TransactionPage, PageOne, NewTransaction, NewAccount, AllTransactions, Holdings):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location; 
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("TransactionPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        self.update()
        frame.tkraise()


if __name__ == "__main__":
    try:
        DAO.updateCompanyList()
        if date.today().month < 4:
            year = date.today().year
        else:
            year = date.today().year+1
        DAO.importDividendsForAll(year)
    except Exception as e:
        print("Couldnt Import Dividends", e)
    app = MyApp()
    app.mainloop()
