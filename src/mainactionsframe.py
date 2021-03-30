from tkinter import *
from tkinter import ttk

from .uiconst import *
from .configdialog import ConfigDialog

class MainActionsFrame(Frame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 

    self.btn_config = Button(self, text='Config', width=BTNW, command=self.config)
    self.btn_config.pack(padx=PADX, pady=PADY, side = 'left')

    self.btn_doc = Button(self, text='Doc', width=BTNW)
    self.btn_doc.pack(padx=PADX, pady=PADY, side = 'left')

    self.btn_exit = Button(self, text='Exit', width=BTNW, command=parent.destroy)
    self.btn_exit.pack(padx=PADX, pady=PADY, side = 'right')


  def config(self):
    cd = ConfigDialog(self.parent)
    # set modal mode
    cd.grab_set()