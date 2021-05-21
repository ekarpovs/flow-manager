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
    self.rowconfigure(3, weight=4)
    self.columnconfigure(0, weight=1)

    # Setup combobox
    self.namesvar = StringVar()
    self.names_combo_box = ttk.Combobox(self, textvariable=self.namesvar)
    self.names_combo_box['state'] = 'readonly'

    # Setup Treeview
    self.flow_tree_view = ttk.Treeview(self, columns=("description"), selectmode="browse")
    # Setup the treview heading
    self.flow_tree_view.heading('#0', text='Operation', anchor=W)
    self.flow_tree_view.heading('#1', text='Parameters', anchor=W)  

    self.flow_tree_view.column('#0', minwidth=70, width=80)

    # Setup operation parameters view
    self.oper_params_view = OperParamsView(self)

    # Setup operation parameters buttons
    oper_actions = Frame(self)
    self.btn_add = Button(oper_actions, text='Add', width=BTNW)
    self.btn_remove = Button(oper_actions, text='Remove', width=BTNW)
    self.btn_reset = Button(oper_actions, text='Reset', width=BTNW)
    self.btn_save = Button(oper_actions, text='Save', width=BTNW)

    self.btn_add.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W + N)   
    self.btn_remove.grid(row=0, column=1, padx=PADX, pady=PADY, sticky=E + N)
    self.btn_reset.grid(row=0, column=2, padx=PADX, pady=PADY, sticky=E + N)
    self.btn_save.grid(row=0, column=3, padx=PADX, pady=PADY, sticky=E + N)


    # Setup flow actions buttons
    # TODO: separate view
    flow_actions = Frame(self)

    self.btn_run = Button(flow_actions, text='Run', width=BTNW)
    self.btn_top = Button(flow_actions, text='Top', width=BTNW)
    self.btn_step = Button(flow_actions, text='Step', width=BTNW)
    self.btn_back = Button(flow_actions, text='Back', width=BTNW)

    self.btn_run.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W + N)
    self.btn_step.grid(row=0, column=2, padx=PADX, pady=PADY, sticky=W + N)
    self.btn_back.grid(row=0, column=3, padx=PADX, pady=PADY, sticky=E + N)
    self.btn_top.grid(row=0, column=4, padx=PADX, pady=PADY, sticky=E + N)

    # Setup widgets layout
    self.names_combo_box.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=N+S+W+E)
    self.flow_tree_view.grid(row=1, column=0, padx=PADX, pady=PADY, sticky=W + E + S + N)
    oper_actions.grid(row=2, column=0, padx=PADX, pady=PADY, sticky=W + E + S + N)
    self.oper_params_view.grid(row=3, column=0, padx=PADX, pady=PADY, sticky=N+S+W+E)
    flow_actions.grid(row=4, column=0, padx=PADX, pady=PADY, sticky=W + E + S + N)



  def clear_flow_tree_view(self):
    for item in self.flow_tree_view.get_children():
      self.flow_tree_view.delete(item)


  def set_flow_meta(self, flow_meta, idx=0):
    self.clear_flow_tree_view()
    for i, item in enumerate(flow_meta):
      self.flow_tree_view.insert(parent='', index='end', iid=i, text=item)
    self.set_selection_tree(idx)
    
    return

  def set_selection_tree(self, idx=0):
    max_idx = len(self.flow_tree_view.get_children())
    if idx >= max_idx:
      idx = max_idx-1
    self.flow_tree_view.focus_set()
    self.flow_tree_view.selection_set(idx)
    self.flow_tree_view.focus(idx)
    
    return

  def get_current_selection_tree(self):
    idx = self.flow_tree_view.selection()
    idx = int(idx[0])
    
    return idx

  def set_worksheets_names(self, worksheets_names):
    self.names_combo_box['values'] = worksheets_names
    self.names_combo_box.current(0)

    return


  def set_operation_params(self, idx, exec, oper_params):
    self.oper_params_view.set_operation_params(idx, exec, oper_params)

    return

  def clear_operation_params(self):
    self.oper_params_view.clear_operation_params()

    return
