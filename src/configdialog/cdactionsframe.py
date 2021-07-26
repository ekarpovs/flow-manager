from tkinter import *
from tkinter import ttk

from ..uiconst import *

class CdActionsFrame(Frame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 

    self.btn_ok = ttk.Button(self, text='Ok', width=BTNW, command=self.Ok)
    self.btn_ok.pack(padx=PADX, pady=PADY, side = 'left')

    self.btn_cancel = ttk.Button(self, text='Cancel', width=BTNW, command=self.Cancel)
    self.btn_cancel.pack(padx=PADX, pady=PADY, side = 'right')

  def Ok(self):
    self.parent.Ok() 
  
  def Cancel(self):
    self.parent.Cancel() 