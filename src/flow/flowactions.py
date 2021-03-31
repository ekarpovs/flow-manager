from tkinter import *
from tkinter import ttk

from ..uiconst import *

class FlowActions(LabelFrame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 

    self['bd'] = 2
    self['relief'] = RIDGE 
    self.parent['bg'] = 'cyan'

    print("ACTIONS")

    self.btn_run = Button(self, text='Run', width=BTNW)
    self.btn_run.pack(padx=PADX, pady=PADY, side = 'left')

    self.btn_step = Button(self, text='Step', width=BTNW)
    self.btn_step.pack(padx=PADX, pady=PADY, side = 'left')

