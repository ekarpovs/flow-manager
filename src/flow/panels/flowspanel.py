from tkinter import *

from ...uiconst import *
from .panel import Panel

class FlowsPanel(Panel):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 

    self['bg'] = "mint cream"
    self['text'] = 'Flows panel'

    self.grid()
    self.rowconfigure(0, weight=1)
    self.rowconfigure(1, weight=1)
    self.columnconfigure(0, weight=1)

    self.flow = []
    self.choicesvar = StringVar(value=self.flow)
    self.flow_list_box = Listbox(self, height=10, listvariable=self.choicesvar)

    # choices.append("peach")
    # choicesvar.set(choices)
    self.flow_list_box.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=S + W + E + N)


  def set_flow(self, flow):
    self.choicesvar.set(flow)
    
    return
