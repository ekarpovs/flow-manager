from tkinter import *
from tkinter import ttk

from .configdialog import ConfigDialog

class ButtonsFrame(LabelFrame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 
    self['text'] = 'Buttons'


    self.btn_config = Button(self, text='Config', width=10, command=self.config)
    self.btn_config.grid(row=0, column=0, padx=10, pady=10)

    self.btn_doc = Button(self, text='Doc', width=10)
    self.btn_doc.grid(row=0, column=1, padx=10, pady=10)

    self.btn_exit = Button(self, text='Exit', width=10, command=parent.destroy)
    self.btn_exit.grid(row=0, column=2, padx=10, pady=10, sticky=E)

    # grid configuration
    self.columnconfigure(2, weight=1)


  def config(self):
    cd = ConfigDialog(self.parent)
    # set modal mode
    cd.grab_set()