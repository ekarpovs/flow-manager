from tkinter import *
from tkinter import ttk

from ...uiconst import *
from .panel import Panel

class FlowsPanel(Panel):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 

    self['bg'] = "mint cream"
    self['text'] = 'Flows panel'

    self.grid()
    # self.rowconfigure(0, weight=1)
    self.rowconfigure(1, weight=1)
    self.columnconfigure(0, weight=1)

    self.namesvar = StringVar()
    self.names_combo_box = ttk.Combobox(self, textvariable=self.namesvar)

    self.flow = []
    self.modulesvar = StringVar(value=self.flow)
    self.flow_list_box = Listbox(self, height=10, listvariable=self.modulesvar)

    # choices.append("peach")
    # choicesvar.set(choices)
    self.names_combo_box.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W + E + N)
    self.flow_list_box.grid(row=1, column=0, padx=PADX, pady=PADY, sticky=W + E + N)

  def set_flow_names(self, names):
    self.names_combo_box['values'] = names

  def set_flow(self, flow):
    self.modulesvar.set(flow)
    
    return

