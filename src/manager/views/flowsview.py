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

    self.namesvar = StringVar()
    self.names_combo_box = ttk.Combobox(self, textvariable=self.namesvar)
    self.names_combo_box['state'] = 'readonly'

    self.flow = []
    self.flowsvar = StringVar(value=self.flow)
    self.flow_list_box = Listbox(self, height=10, listvariable=self.flowsvar, selectmode=BROWSE)

    self.oper_params_view = OperParamsView(self)

    self.names_combo_box.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=N+S+W+E)
    self.flow_list_box.grid(row=1, column=0, padx=PADX, pady=PADY, sticky=N+S+W+E)

    oper_actions = Frame(self)
    oper_actions.grid(row=2, column=0, padx=PADX, pady=PADY, sticky=W + E + S + N)
    self.btn_add = Button(oper_actions, text='Add', width=BTNW)
    self.btn_remove = Button(oper_actions, text='Remove', width=BTNW)
    self.btn_reset = Button(oper_actions, text='Reset', width=BTNW)
    self.btn_save = Button(oper_actions, text='Save', width=BTNW)

    self.btn_add.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W + N)   
    self.btn_remove.grid(row=0, column=1, padx=PADX, pady=PADY, sticky=E + N)
    self.btn_reset.grid(row=0, column=2, padx=PADX, pady=PADY, sticky=E + N)
    self.btn_save.grid(row=0, column=3, padx=PADX, pady=PADY, sticky=E + N)

    self.oper_params_view.grid(row=3, column=0, padx=PADX, pady=PADY, sticky=N+S+W+E)


    self.flow_tree_view = ttk.Treeview(self, columns=("description"))
    self.flow_tree_view.heading('#0', text='Operation')
    self.flow_tree_view.heading('#1', text='Parameters')

    # Inserted at the root, program chooses id:
    # self.flow_tree_view.insert(parent='', index='end', text='clrs.brgto')
    # self.flow_tree_view.insert(parent='', index='end', text='blur.gaus')
    # self.flow_tree_view.insert(parent='', index='end', text='edge.canny')
    # self.flow_tree_view.insert(parent='', index='end', text='edge.laplacian')

    
    
    self.flow_tree_view.grid(row=4, column=0, padx=PADX, pady=PADY, sticky=W + E + S + N)



    # TODO: separate view
    flow_actions = Frame(self)
    flow_actions.grid(row=5, column=0, padx=PADX, pady=PADY, sticky=W + E + S + N)

    self.btn_run = Button(flow_actions, text='Run', width=BTNW)
    self.btn_top = Button(flow_actions, text='Top', width=BTNW)
    self.btn_step = Button(flow_actions, text='Step', width=BTNW)
    self.btn_back = Button(flow_actions, text='Back', width=BTNW)

    self.btn_run.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W + N)
    self.btn_step.grid(row=0, column=2, padx=PADX, pady=PADY, sticky=W + N)
    self.btn_back.grid(row=0, column=3, padx=PADX, pady=PADY, sticky=E + N)
    self.btn_top.grid(row=0, column=4, padx=PADX, pady=PADY, sticky=E + N)



  def set_tree_flow_meta(self, flow_meta):
    for item in flow_meta:
      self.flow_tree_view.insert(parent='', index='end', text=item)

    return

  def set_worksheets_names(self, worksheets_names):
    self.names_combo_box['values'] = worksheets_names
    self.names_combo_box.current(0)

  def set_flow_meta(self, flow_meta):
    self.flowsvar.set(flow_meta)
    self.set_selection()
    self.set_tree_flow_meta(flow_meta)

    return

  def set_selection(self, idx=0):
    self.flow_list_box.focus_set()
    cur_idx = self.flow_list_box.curselection()
    if len(cur_idx) == 0:
      cur_idx = 0
    self.flow_list_box.selection_clear(cur_idx, cur_idx)
    self.select_list_item(idx)
    
    return


  def select_list_item(self, idx):
    self.flow_list_box.activate(idx)
    self.flow_list_box.selection_set(ACTIVE)
    self.flow_list_box.see(idx)
    self.flow_list_box.event_generate("<<ListboxSelect>>")


    return


  def set_operation_params(self, idx, exec, oper_params):
    self.oper_params_view.set_operation_params(idx, exec, oper_params)

    return

  def clear_operation_params(self):
    self.oper_params_view.clear_operation_params()

    return
