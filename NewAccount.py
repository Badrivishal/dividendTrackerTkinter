import tkinter as tk
from tkinter import font as tkfont
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import ttk
from application import *
from pageOne import *
from StartPage import *
import DAO
import app

class NewAccount(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        button = tk.Button(self, text="Back",command=lambda: controller.show_frame("StartPage"))
        button.grid(column=0, row=0)

        lbl = tk.Label(self, text = "New Account")
        lbl.grid(column = 1, row = 0, columnspan = 12)
        
        lbl2 = tk.Label(self, text = "Account Name")
        lbl2.grid(column=0, row=1)
        
        self.accountNameEntryBox = tk.Entry(self)
        self.accountNameEntryBox.grid(column=1, row=1)
        


        button = tk.Button(self, text="Submit",
                           command=self.createNewAccountButton)
        button.grid(column=0, row=2)

    def createNewAccountButton(self):
        DAO.newAccount(self.accountNameEntryBox.get())
        self.accountNameEntryBox.delete(0, 'end')
        self.controller.show_frame("StartPage")
