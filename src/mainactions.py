from tkinter import *
from tkinter import ttk

from .uiconst import *
from .configdialog import ConfigDialog

class MainActions(Frame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 

    self["bg"] = "green"

    self.grid()
    self.rowconfigure(0, weight=1)
    self.columnconfigure(2, weight=1)

    self.btn_config = Button(self, text='Config', width=BTNW, command=self.config)
    self.btn_config.grid(row=0, column=0, padx=PADX, pady=PADY)

    self.btn_doc = Button(self, text='Doc', width=BTNW)
    self.btn_doc.grid(row=0, column=1, padx=PADX, pady=PADY)

    self.btn_exit = Button(self, text='Exit', width=BTNW)
    self.btn_exit.grid(row=0, column=2, padx=PADX, pady=PADY, sticky=E)


  def config(self):
    cd = ConfigDialog(self.parent)
    # set modal mode
    cd.grab_set()