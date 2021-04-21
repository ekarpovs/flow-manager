from os import read
from src.manager.views.operparamsview import OperParamsView
from tkinter import *
from tkinter import ttk

from ...uiconst import *
from .view import View

class FlowsView(View):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 

    self['bg'] = "mint cream"
    self['text'] = 'Flows panel'

    self.grid()
    self.rowconfigure(1, weight=1)
    self.rowconfigure(2, weight=4)
    self.columnconfigure(0, weight=1)

    self.namesvar = StringVar()
    self.names_combo_box = ttk.Combobox(self, textvariable=self.namesvar)
    self.names_combo_box['state'] = 'readonly'

    self.flow = []
    self.modulesvar = StringVar(value=self.flow)
    self.flow_list_box = Listbox(self, height=10, listvariable=self.modulesvar, selectmode=BROWSE)

    self.oper_params_view = OperParamsView(self)

    self.btn_load = Button(self, text='Load', width=BTNW)
    self.btn_run = Button(self, text='Run', width=BTNW)
    self.btn_step = Button(self, text='Step', width=BTNW)
    self.btn_back = Button(self, text='Back', width=BTNW)
    self.btn_top = Button(self, text='Top', width=BTNW)

    self.names_combo_box.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=N+S+W+E)
    self.flow_list_box.grid(row=1, column=0, padx=PADX, pady=PADY, sticky=N+S+W+E)

    self.oper_params_view.grid(row=2, column=0, padx=PADX, pady=PADY, sticky=N+S+W+E)

    # TODO: separate view
    self.btn_load.grid(row=3, column=0, padx=PADX, pady=PADY, sticky=W + S)
    self.btn_run.grid(row=4, column=0, padx=PADX, pady=PADY, sticky=W + S)
    self.btn_step.grid(row=5, column=0, padx=PADX, pady=PADY, sticky=W + S)
    self.btn_back.grid(row=6, column=0, padx=PADX, pady=PADY, sticky=W + S)
    self.btn_top.grid(row=7, column=0, padx=PADX, pady=PADY, sticky=W + S)



  def set_worksheets_names(self, worksheets_names):
    self.names_combo_box['values'] = worksheets_names
    self.names_combo_box.current(0)

  def set_flow_meta(self, flow_meta):
    self.modulesvar.set(flow_meta)
    self.set_first_selection()

    return

  def set_first_selection(self):
    idx = self.flow_list_box.curselection()
    if len(idx) == 0:
      idx = 0
    self.flow_list_box.selection_clear(idx, idx)
    self.select_list_item(0)
    
    return


  def select_list_item(self, idx):
    self.flow_list_box.activate(idx)
    self.flow_list_box.selection_set(ACTIVE)
    self.flow_list_box.see(idx)

    return

  def set_next_selection(self, back=False):
    idx = self.flow_list_box.curselection()
    print("Next selection", idx)
    if len(idx) == 0:
      next_idx = 0
    else:
      if back:
        next_idx = idx[0]-1
      else:
        next_idx = idx[0]+1

      self.flow_list_box.selection_clear(idx, idx)
    
    self.select_list_item(next_idx)
    
    return


  def set_operation_params(self, idx, exec, oper_params):
    self.oper_params_view.set_operation_params(idx, exec, oper_params)

    return

  def clear_operation_params(self):
    self.oper_params_view.clear_operation_params()

    return
