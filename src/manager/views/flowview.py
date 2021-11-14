from typing import List, Dict, Tuple
from tkinter import *
from tkinter import ttk
from tkscrolledframe import ScrolledFrame

from ...uiconst import *
from .view import View
from src.manager.views.operparamsview import OperParamsView

class FlowView(View):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 
    # self['bg'] = "mint cream"
    self['text'] = 'Flows'

    self.grid()
    self.rowconfigure(1, weight=1)
    self.rowconfigure(3, weight=4)
    self.columnconfigure(0, weight=1)

    # Setup combobox
    self.namesvar = StringVar()
    self.names_combo_box = ttk.Combobox(self, textvariable=self.namesvar, font=("TkDefaultFont"))
    self.names_combo_box['state'] = 'readonly'

    # Setup Treeview
    self.flow_tree_view = ttk.Treeview(self, columns=("description"), selectmode="browse")
    # Setup the treview heading
    self.flow_tree_view.heading('#0', text='Exec/Statement', anchor=W)
    self.flow_tree_view.heading('#1', text='Parameters', anchor=W)  

    self.flow_tree_view.column('#0', minwidth=70, width=80)

    self.tree_view_scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=self.flow_tree_view.yview)
    self.tree_view_scrollbar.grid(row=1, column=1, sticky=N+S)
    self.flow_tree_view.configure(yscrollcommand=self.tree_view_scrollbar.set)

    # Setup operation parameters view
    # Create a ScrolledFrame widget
    sf = ScrolledFrame(self)
    # Bind the arrow keys and scroll wheel
    sf.bind_arrow_keys(self)
    sf.bind_scroll_wheel(self)
    # Create a frame within the ScrolledFrame
    self.oper_params_view = sf.display_widget(OperParamsView)

    # Setup operation buttons
    oper_actions = Frame(self)
    self.btn_add = ttk.Button(oper_actions, text='Add', width=BTNW)
    self.btn_remove = ttk.Button(oper_actions, text='Remove', width=BTNW)
    self.btn_reset = ttk.Button(oper_actions, text='Reset', width=BTNW)
    self.btn_save = ttk.Button(oper_actions, text='Save', width=BTNW)

    self.btn_add.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W + N)   
    self.btn_remove.grid(row=0, column=1, padx=PADX, pady=PADY, sticky=E + N)
    self.btn_reset.grid(row=0, column=2, padx=PADX, pady=PADY, sticky=E + N)
    self.btn_save.grid(row=0, column=3, padx=PADX, pady=PADY, sticky=E + N)

    # Setup flow actions buttons
    # TODO: separate view
    flow_actions = Frame(self)

    self.btn_run = ttk.Button(flow_actions, text='Run', width=BTNW)
    self.btn_next = ttk.Button(flow_actions, text='Next', width=BTNW)
    self.btn_prev = ttk.Button(flow_actions, text='Prev', width=BTNW)
    self.btn_top = ttk.Button(flow_actions, text='Top', width=BTNW)

    self.btn_run.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W + N)
    self.btn_next.grid(row=0, column=1, padx=PADX, pady=PADY, sticky=W + N)
    self.btn_prev.grid(row=0, column=2, padx=PADX, pady=PADY, sticky=E + N)
    self.btn_top.grid(row=0, column=3, padx=PADX, pady=PADY, sticky=E + N)
    # Setup widgets layout
    self.names_combo_box.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=N+S+W+E)
    self.flow_tree_view.grid(row=1, column=0, padx=PADX, pady=PADY, sticky=W + E + S + N)
    oper_actions.grid(row=2, column=0, padx=PADX, pady=PADY, sticky=W + E + S + N)
    sf.grid(row=3, column=0, padx=PADX, pady=PADY, sticky=N+S+W+E)
    flow_actions.grid(row=4, column=0, padx=PADX, pady=PADY, sticky=W + E + S + N)
    # Set the buttons initial state
    self.activate_buttons()
    return


  def clear_flow_tree_view(self):
    items = self.flow_tree_view.get_children()
    for item in items:
      self.flow_tree_view.delete(item)
    return
    
  def set_flow_item_names(self, flow_names, idx=0):
    self.clear_flow_tree_view()
    for i, name in enumerate(flow_names):
      self.flow_tree_view.insert(parent='', index='end', iid=i, text=name)
    self.set_selection_tree(idx)  
    return

  def set_selection_tree(self, idx=0):
    max_idx = len(self.flow_tree_view.get_children())
    if max_idx == 0:
      return
    if idx >= max_idx:
      idx = max_idx-1
    self.flow_tree_view.focus_set()
    self.flow_tree_view.selection_set(idx)
    self.flow_tree_view.focus(idx)   
    return

  def get_current_selection_tree(self) -> Tuple[int, str]:
    idx = self.flow_tree_view.selection()
    if len(idx) > 0:
      idx = int(idx[0])
    else:
      idx = 0
    cur_item = self.flow_tree_view.focus()
    item = self.flow_tree_view.item(cur_item)  
    return (idx, item.get('text'))
  
  # def get_current_tree_item(self) -> str:
  #   cur_item = self.flow_tree_view.focus()
  #   return self.flow_tree_view.item(cur_item)  

  @property
  def ws_names(self) -> List[str]:
    return self.names_combo_box.get('values')

  @ws_names.setter
  def ws_names(self, ws_names: List[str]) ->None:
    self.names_combo_box['values'] = ws_names
    self.names_combo_box.current(0)
    return

  # Parameter subpanel Wrappers
  def get_operation_params_item(self) -> List[Dict]: 
    return self.oper_params_view.get_operation_params_item()

  def set_operation_params(self, idx, name, params, params_def):
    self.oper_params_view.set_operation_params_from_dict(idx, name, params, params_def)
    return

  def reset_operation_params(self, idx, exec, oper_params):
    self.oper_params_view.set_operation_params(idx, exec, oper_params)
    return

  def clear_operation_params(self):
    self.oper_params_view.clear_operation_params()
    return

  def activate_buttons(self, activate=False):
    state = DISABLED
    if activate:
      state = NORMAL
    self.btn_run['state']=state
    self.btn_next['state']=state
    self.btn_prev['state']=state
    self.btn_top['state']=state
    return
