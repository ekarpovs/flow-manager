from tkinter import * 

from ..uiconst import *
from .cdactionsframe import CdActionsFrame

class ConfigDialog(Toplevel):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent

    # self.positionfrom(parent)
    self.title('Configuration')
    self.geometry("500x300+%d+%d" % (parent.winfo_rootx() + 20,
      parent.winfo_rooty() + 30))
    self.resizable(height=FALSE, width=FALSE) 

    # self.columnconfigure(0, weight=1)
    # self.columnconfigure(1, weight=1)
    # self.rowconfigure(0, weight=5)
    # self.rowconfigure(1, weight=1)

    self.content_frame = Frame(self, bd=2, relief=RIDGE)
    self.content_frame.grid(row=0, column=0, columnspan=2, padx=PADX, pady=PADY, sticky=E+W+N+S)

    self.actions_frame = CdActionsFrame(self)
    self.actions_frame.grid(row=1, column=0, columnspan=2, padx=PADX, pady=PADY, sticky=W+E+S)

  def Ok(self):
    print("Saved!") 
  
  def Cancel(self):
    self.destroy() 