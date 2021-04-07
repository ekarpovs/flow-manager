from os import read
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
    self.names_combo_box['state'] = 'readonly'

    self.flow = []
    self.modulesvar = StringVar(value=self.flow)
    self.flow_list_box = Listbox(self, height=10, listvariable=self.modulesvar)

    self.btn_load = Button(self, text='Load', width=BTNW)
    self.btn_run = Button(self, text='Run', width=BTNW)
    self.btn_step = Button(self, text='Step', width=BTNW)

    self.names_combo_box.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W + E + N)
    self.flow_list_box.grid(row=1, column=0, padx=PADX, pady=PADY, sticky=W + E + N)
    self.btn_load.grid(row=2, column=0, padx=PADX, pady=PADY, sticky=W + S)
    self.btn_run.grid(row=3, column=0, padx=PADX, pady=PADY, sticky=W + S)
    self.btn_step.grid(row=4, column=0, padx=PADX, pady=PADY, sticky=W + S)



  def set_work_sheet_names(self, work_sheet_names):
    self.names_combo_box['values'] = work_sheet_names
    self.names_combo_box.current(0)
    # self.names_combo_box.set(work_sheet_names[0])

  def set_work_sheet(self, work_sheet):
    self.modulesvar.set(work_sheet['steps'])
    
    return


