import tkinter as tk
from tkinter import font as tkfont
from NewAccount import *
from application import *
from pageOne import *
from TransactionPage import *
from NewTransaction import *



class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.attributes('-fullscreen',True)

        self.title_font = tkfont.Font(family='Helvetica', size=25, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (TransactionPage, PageOne, NewTransaction, NewAccount):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location; 
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("TransactionPage")
        # frame.tkraise()

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        self.update()
        frame.tkraise()


if __name__ == "__main__":
    DAO.updateCompanyList()
    app = MyApp()
    app.mainloop()
