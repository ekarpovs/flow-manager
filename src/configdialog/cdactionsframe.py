from tkinter import *
from tkinter import ttk

class CdActionsFrame(Frame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 

    # grid configuration
    self.columnconfigure(1, weight=1)

    self.button_ok = Button(self, text='Ok', width=10, command=self.Ok)
    self.button_ok.grid(row=0, column=0)

    self.button_cancel = Button(self, text='Cancel', width=10, command=self.Cancel)
    self.button_cancel.grid(row=0, column=1, sticky=E)

  def Ok(self):
    self.parent.Ok() 
  
  def Cancel(self):
    self.parent.Cancel() 