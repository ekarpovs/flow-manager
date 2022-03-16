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
    self.rowconfigure(0, weight=1)
    self.rowconfigure(1, weight=1)
    self.rowconfigure(2, weight=1)
    self.rowconfigure(3, weight=1)
    self.rowconfigure(4, weight=4)
    self.rowconfigure(5, weight=1)
    self.columnconfigure(0, weight=10)
    self.columnconfigure(1, weight=1)

    # Setup flow names list view
    self._flow_names_frame = Frame(self, highlightbackground='gray', highlightthickness=1)
    self._flow_names_frame.columnconfigure(0, weight=5)
    self._flow_names_frame.columnconfigure(1, weight=1)
    # setup combo box
    self._namesvar = StringVar()
    self.names_combo_box = Combobox(self._flow_names_frame, textvariable=self._namesvar, font=("TkDefaultFont"))
    self.names_combo_box['state'] = 'readonly'
    # setup button
    self.btn_reload = Button(self._flow_names_frame, text='Reload', width=BTNW_S)
    self.names_combo_box.grid(row=0, column=0, padx=PADX, sticky=W+E)
    self.btn_reload.grid(row=0, column=1, padx=PADX, pady=PADY, sticky=E)   

    # Setup flow steps view
    self._flow_steps_frame = Frame(self, highlightbackground='gray', highlightthickness=1)
    self._flow_steps_frame.columnconfigure(0, weight=5)
    self._flow_steps_frame.columnconfigure(1, weight=1)
    self._flow_steps_frame.rowconfigure(0, weight=5)
    self._flow_steps_frame.rowconfigure(1, weight=1)
    # setup Treeview
    self.flow_tree_view = Treeview(self._flow_steps_frame, columns=['#0','#1','#2'], selectmode="browse")
    # setup the treview heading
    self.flow_tree_view.heading('#0', text='Index', anchor=CENTER)
    self.flow_tree_view.heading('#1', text='Exec/Statement', anchor=W)
    self.flow_tree_view.heading('#2', text='Title', anchor=W)  
    self.flow_tree_view.column('#0', minwidth=30, width=40)
    self.flow_tree_view.column('#1', minwidth=120, width=140)
    self.flow_tree_view.column('#2', minwidth=250, width=400)
    self.flow_tree_view.grid(row=0, column=0, columnspan=2, padx=PADX, pady=PADY,sticky=W+E+S+N)   
    # setup scrollbars
    self.tree_view_scrollbar_y = Scrollbar(self._flow_steps_frame, orient=VERTICAL, command=self.flow_tree_view.yview)
    self.tree_view_scrollbar_y.grid(row=0, column=1, sticky=N+S+E)
    self.flow_tree_view.configure(yscrollcommand=self.tree_view_scrollbar_y.set)   
    self.tree_view_scrollbar_x = Scrollbar(self._flow_steps_frame, orient=HORIZONTAL, command=self.flow_tree_view.xview)
    self.tree_view_scrollbar_x.grid(row=1, column=0, columnspan=3, sticky=S+W+E)
    self.flow_tree_view.configure(xscrollcommand=self.tree_view_scrollbar_x.set)

    # Setup operation parameters view
    self._params_view_frame = Frame(self, highlightbackground='gray', highlightthickness=1)
    self._params_view_frame.columnconfigure(0, weight=1)
    self._params_view_frame.rowconfigure(0, weight=1)
    # Create a ScrolledFrame widget
    self._params = ScrolledFrame(self._params_view_frame)
    self._params.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=N+S+W+E)

    # Bind the arrow keys and scroll wheel
    self._params.bind_arrow_keys(self._params)
    self._params.bind_scroll_wheel(self._params)
    # Create a frame within the ScrolledFrame
    self.oper_params_view_frame = self._params.display_widget(OperParamsView)

    # Setup operation actions view
    self._oper_actions_frame = Frame(self, highlightbackground='gray', highlightthickness=1)
    self.btn_add = Button(self._oper_actions_frame, text='Add', width=BTNW_S)
    self.btn_remove = Button(self._oper_actions_frame, text='Remove', width=BTNW_S)
    self.btn_reset = Button(self._oper_actions_frame, text='Reset', width=BTNW_S)
    self.btn_save = Button(self._oper_actions_frame, text='Save', width=BTNW_S)
    self.btn_links = Button(self._oper_actions_frame, text='Links', width=BTNW_S)

    self.btn_add.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W + N)   
    self.btn_remove.grid(row=0, column=1, padx=PADX, pady=PADY, sticky=E + N)
    self.btn_reset.grid(row=0, column=2, padx=PADX, pady=PADY, sticky=E + N)
    self.btn_save.grid(row=0, column=3, padx=PADX, pady=PADY, sticky=E + N)
    self.btn_links.grid(row=0, column=4, padx=PADX, pady=PADY, sticky=E + N)

    # Setup param actions view
    self._param_actions_frame = Frame(self, highlightbackground='gray', highlightthickness=1)
    self.btn_params_reset = Button(self._param_actions_frame, text='Reset', width=BTNW_S)
    self.btn_params_default = Button(self._param_actions_frame, text='Default', width=BTNW_S)
    self.btn_params_io = Button(self._param_actions_frame, text='I/O', width=BTNW_S)
    self.btn_params_reset.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W+N)
    self.btn_params_default.grid(row=0, column=1, padx=PADX, pady=PADY, sticky=W+N)
    self.btn_params_io.grid(row=0, column=2, padx=PADX, pady=PADY, sticky=W+N)

    # Setup flow actions buttons
    self._flow_actions_frame = Frame(self, highlightbackground='gray', highlightthickness=1)
    self.btn_run = Button(self._flow_actions_frame, text='Run', width=BTNW_S)
    self.btn_curr = Button(self._flow_actions_frame, text='Current', width=BTNW_S)
    self.btn_next = Button(self._flow_actions_frame, text='Next', width=BTNW_S)
    self.btn_prev = Button(self._flow_actions_frame, text='Prev', width=BTNW_S)
    self.btn_top = Button(self._flow_actions_frame, text='Top', width=BTNW_S)

    self.btn_run.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W + N)
    self.btn_curr.grid(row=0, column=1, padx=PADX, pady=PADY, sticky=W + N)
    self.btn_next.grid(row=0, column=2, padx=PADX, pady=PADY, sticky=W + N)
    self.btn_prev.grid(row=0, column=3, padx=PADX, pady=PADY, sticky=E + N)
    self.btn_top.grid(row=0, column=4, padx=PADX, pady=PADY, sticky=E + N)

    # Setup widgets groups layout
    self._flow_names_frame.grid(row=0, column=0, columnspan=2, padx=PADX, sticky=W+E)
    self._flow_steps_frame.grid(row=1, column=0, columnspan=2, padx=PADX, sticky=W+E+S+N)   
    self._oper_actions_frame.grid(row=2, column=0, columnspan=2, padx=PADX, sticky=W+E)
    self._param_actions_frame.grid(row=3, column=0, columnspan=2, padx=PADX, sticky=W+E)
    self._params_view_frame.grid(row=4, column=0, columnspan=2,padx=PADX, sticky=N+S+W+E)
    self._flow_actions_frame.grid(row=5, column=0, columnspan=2, padx=PADX, sticky=W+E)
    # Set the buttons initial state
    self.activate_buttons()
    return


  def clear_flow_tree_view(self):
    items = self.flow_tree_view.get_children()
    for item in items:
      self.flow_tree_view.delete(item)
    return
    
  def set_flow_item_names(self, flow_names, flow_titles, idx=0):
    self.clear_flow_tree_view()
    for i, name in enumerate(flow_names):
      idx_s = f'{i:02}'
      self.flow_tree_view.insert(parent='', index='end', iid=i, text=idx_s, values=[name, flow_titles[i]])
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
    self.flow_tree_view.see(idx) 
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
    return self.oper_params_view_frame.get_current_operation_params_def()

  def get_current_opreation_params_idx(self) -> int:
    return self.oper_params_view_frame.get_current_opreation_params_idx()

  def get_current_operation_param_control(self, cname) -> Widget:
    return self.oper_params_view_frame.get_current_operation_param_control(cname)

  def create_operation_params_controls(self, idx, name, params, params_def):
    self.oper_params_view_frame.create_operation_params_controls(idx, name, params, params_def)
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
    self.btn_params_io['state']=state
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