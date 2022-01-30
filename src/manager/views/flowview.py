from re import A
from typing import Callable, List, Dict, Tuple
from tkinter import *
from tkinter.ttk import Combobox, Treeview, Button 
from tkscrolledframe import ScrolledFrame

from src.manager.linksdialog.linksdialog import LinksDialog
from src.manager.models.flow.currentflowmodel import CurrentFlowModel

from ...uiconst import *
from .view import View
from .operparamsview import OperParamsView

class FlowView(View):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 
    self['text'] = 'Flows'

    self.grid()
    self.rowconfigure(1, weight=1)
    self.rowconfigure(4, weight=4)
    self.columnconfigure(0, weight=10)
    self.columnconfigure(1, weight=1)

    # Setup combobox
    self.namesvar = StringVar()
    self.names_combo_box = Combobox(self, textvariable=self.namesvar, font=("TkDefaultFont"))
    self.names_combo_box['state'] = 'readonly'
    self.btn_reload = Button(self, text='Reload', width=BTNW_S)

    # Setup Treeview
    self.flow_tree_view = Treeview(self, columns=("description"), selectmode="browse")
    # Setup the treview heading
    self.flow_tree_view.heading('#0', text='Exec/Statement', anchor=W)
    # self.flow_tree_view.heading('#1', text='Parameters', anchor=W)  
    self.flow_tree_view.column('#0', minwidth=90, width=100)
    self.tree_view_scrollbar = Scrollbar(self, orient=VERTICAL, command=self.flow_tree_view.yview)
    self.tree_view_scrollbar.grid(row=1, column=1, sticky=N+S+E)
    self.flow_tree_view.configure(yscrollcommand=self.tree_view_scrollbar.set)

    # Setup operation parameters view
    # Create a ScrolledFrame widget
    self.params = ScrolledFrame(self)
    # Bind the arrow keys and scroll wheel
    self.params.bind_arrow_keys(self)
    self.params.bind_scroll_wheel(self)
    # Create a frame within the ScrolledFrame
    self.oper_params_view = self.params.display_widget(OperParamsView)

    # Setup operation buttons
    oper_actions = Frame(self, highlightbackground='gray', highlightthickness=1)
    self.btn_add = Button(oper_actions, text='Add', width=BTNW_S)
    self.btn_remove = Button(oper_actions, text='Remove', width=BTNW_S)
    self.btn_reset = Button(oper_actions, text='Reset', width=BTNW_S)
    self.btn_save = Button(oper_actions, text='Save', width=BTNW_S)
    self.btn_links = Button(oper_actions, text='Links', width=BTNW_S)

    self.btn_add.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W + N)   
    self.btn_remove.grid(row=0, column=1, padx=PADX, pady=PADY, sticky=E + N)
    self.btn_reset.grid(row=0, column=2, padx=PADX, pady=PADY, sticky=E + N)
    self.btn_save.grid(row=0, column=3, padx=PADX, pady=PADY, sticky=E + N)
    self.btn_links.grid(row=0, column=4, padx=PADX, pady=PADY, sticky=E + N)

    # Setup param actions buttons
    param_actions = Frame(self, highlightbackground='gray', highlightthickness=1)
    self.btn_params_reset = Button(param_actions, text='Reset', width=BTNW_S)
    self.btn_params_default = Button(param_actions, text='Default', width=BTNW_S)
    self.btn_params_reset.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W+N)
    self.btn_params_default.grid(row=0, column=1, padx=PADX, pady=PADY, sticky=W+N)

    # Setup flow actions buttons
    flow_actions = Frame(self, highlightbackground='gray', highlightthickness=1)
    self.btn_run = Button(flow_actions, text='Run', width=BTNW_S)
    self.btn_curr = Button(flow_actions, text='Current', width=BTNW_S)
    self.btn_next = Button(flow_actions, text='Next', width=BTNW_S)
    self.btn_prev = Button(flow_actions, text='Prev', width=BTNW_S)
    self.btn_top = Button(flow_actions, text='Top', width=BTNW_S)

    self.btn_run.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W + N)
    self.btn_curr.grid(row=0, column=1, padx=PADX, pady=PADY, sticky=W + N)
    self.btn_next.grid(row=0, column=2, padx=PADX, pady=PADY, sticky=W + N)
    self.btn_prev.grid(row=0, column=3, padx=PADX, pady=PADY, sticky=E + N)
    self.btn_top.grid(row=0, column=4, padx=PADX, pady=PADY, sticky=E + N)

    # Setup widgets layout
    self.names_combo_box.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=N+S+W+E)
    self.btn_reload.grid(row=0, column=1, padx=PADX, pady=PADY, sticky=N+S+W+E)   
    self.flow_tree_view.grid(row=1, column=0, columnspan=2, padx=PADX, pady=PADY, sticky=W + E + S + N)   
    oper_actions.grid(row=2, column=0, columnspan=2, padx=PADX, pady=PADY, sticky=W + E + S + N)
    param_actions.grid(row=3, column=0, columnspan=2, padx=PADX, pady=PADY, sticky=W + E + S + N)
    self.params.grid(row=4, column=0, columnspan=2,padx=PADX, pady=PADY, sticky=N+S+W+E)
    flow_actions.grid(row=5, column=0, columnspan=2, padx=PADX, pady=PADY, sticky=W + E + S + N)
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
    # self.set_selection_tree(idx)  
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

  def get_current_operation_params_def(self) -> List[Dict]: 
    return self.oper_params_view.get_current_operation_params_def()

  def get_current_opreation_params_idx(self) -> int:
    return self.oper_params_view.get_current_opreation_params_idx()

  def get_current_operation_param_control(self, cname) -> Widget:
    return self.oper_params_view.get_current_operation_param_control(cname)

  def create_operation_params_controls(self, idx, name, params, params_def):
    self.oper_params_view.create_operation_params_controls(idx, name, params, params_def)
    return

  def activate_edit_buttons(self, activate=False) -> None:
    state = DISABLED
    if activate:
      state = NORMAL
    self.btn_add['state']=state
    self.btn_remove['state']=state
    self.btn_reset['state']=state
    self.btn_save['state']=state
    self.btn_links['state']=state
    return

  def activate_params_buttons(self, activate=False) -> None:
    state = DISABLED
    if activate:
      state = NORMAL
    self.btn_params_reset['state']=state
    self.btn_params_default['state']=state
    return

  def activate_runtime_buttons(self, activate=False) -> None:
    state = DISABLED
    if activate:
      state = NORMAL
    self.btn_run['state']=state
    self.btn_curr['state']=state
    self.btn_next['state']=state
    self.btn_prev['state']=state
    self.btn_top['state']=state
    return

  def activate_buttons(self, activate=False) -> None:
    self.activate_edit_buttons(activate)
    self.activate_params_buttons(activate)
    self.activate_runtime_buttons(activate)
    return

  def edit_flow_links(self, flow: CurrentFlowModel, callback: Callable) -> None:
    lnk_dlg = LinksDialog(self.parent, flow, callback)
    return