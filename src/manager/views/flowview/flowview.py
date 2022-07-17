from re import A
from typing import Callable, List, Dict, Tuple
from tkinter import *
from tkinter.ttk import Combobox, Treeview, Button 
from tkscrolledframe import ScrolledFrame

from src.manager.linksdialog.linksdialog import LinksDialog
from src.manager.models.flow.currentflowmodel import CurrentFlowModel

from ....uiconst import *
from ..view import View

class FlowView(View):
  def __init__(self, parent):
    View.__init__(self, parent)
    self['text'] = 'Flows'

    h = int(self._manager_container_h * 0.7)
    w = int((self._manager_container_w / 4)*0.95)
    self['height'] = h
    self['width'] = w

    self._h = h

    # Setup the view
    self.grid_propagate(False)
    self._setup_view()
    
    # Set the buttons initial state
    self.activate_buttons()
    return

# Setup the view
  def _setup_view(self) -> None:
    self._grid_config()
    self._setup_flow_names_view()
    self._setup_flow_items_view()
    self._setup_flow_items_actions_view()
    # self._setup_flow_items_links_view()
    self._setup_flow_actions_view()
    self._setup_views_layout()
    return

  def _grid_config(self) -> None:
    self.grid()
    self.rowconfigure(0, weight=1)
    self.rowconfigure(1, weight=1)
    self.rowconfigure(2, weight=1)
    self.rowconfigure(3, weight=1)
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)
    return

  def _setup_flow_names_view(self) -> None:
    # Setup flow names list view
    fr_h = int(self._h*0.12)
    self._flow_names_frame = Frame(self, height=fr_h,highlightbackground='gray', highlightthickness=1)
    self._flow_names_frame.rowconfigure(0, weight=1)
    self._flow_names_frame.columnconfigure(0, weight=5)
    self._flow_names_frame.columnconfigure(1, weight=1)
    self._flow_names_frame.grid_propagate(False)
    # setup combo box
    self._namesvar = StringVar()
    self.names_combo_box = Combobox(self._flow_names_frame, textvariable=self._namesvar, font=("TkDefaultFont"))
    self.names_combo_box['state'] = 'readonly'
    # setup button
    self.btn_reload = Button(self._flow_names_frame, text='Reload', width=BTNW_S)
    self.names_combo_box.grid(row=0, column=0, padx=PADX, pady=PADY_S, sticky=W+E)
    self.btn_reload.grid(row=0, column=1, padx=PADX, pady=PADY_S, sticky=E)
    return

  def _setup_flow_items_view(self) -> None:
    # Setup flow items view
    fr_h = int(self._h*0.82)
    self._flow_items_frame = Frame(self, height=fr_h, highlightbackground='gray', highlightthickness=1)
    self._flow_items_frame.columnconfigure(0, weight=1)
    self._flow_items_frame.columnconfigure(1, weight=1)
    self._flow_items_frame.rowconfigure(0, weight=1)
    self._flow_items_frame.rowconfigure(1, weight=1)
    self._flow_items_frame.grid_propagate(False)
    # setup Treeview
    self.flow_tree_view = Treeview(self._flow_items_frame, columns=['#0','#1','#2'], selectmode="browse")
    # setup the treview heading
    self.flow_tree_view.heading('#0', text='Index', anchor=CENTER)
    self.flow_tree_view.heading('#1', text='Exec/Statement', anchor=W)
    self.flow_tree_view.heading('#2', text='Title', anchor=W)  
    self.flow_tree_view.column('#0', minwidth=30, width=40)
    self.flow_tree_view.column('#1', minwidth=120, width=140)
    self.flow_tree_view.column('#2', minwidth=250, width=400)
    self.flow_tree_view.grid(row=0, column=0, rowspan=2, columnspan=2, pady=PADY_S,sticky=W+E+S+N)   
    # setup scrollbars
    self.tree_view_scrollbar_y = Scrollbar(self._flow_items_frame, orient=VERTICAL, command=self.flow_tree_view.yview)
    self.tree_view_scrollbar_y.grid(row=0, column=1, rowspan=2, sticky=N+S+E)
    self.flow_tree_view.configure(yscrollcommand=self.tree_view_scrollbar_y.set)   
    self.tree_view_scrollbar_x = Scrollbar(self._flow_items_frame, orient=HORIZONTAL, command=self.flow_tree_view.xview)
    self.tree_view_scrollbar_x.grid(row=1, column=0, columnspan=2, sticky=S+W+E)
    self.flow_tree_view.configure(xscrollcommand=self.tree_view_scrollbar_x.set)
    return

  def _setup_flow_items_actions_view(self) -> None:
    # Setup flow items actions view
    fr_h = int(self._h*0.11)
    self._oper_actions_frame = Frame(self, height=fr_h, highlightbackground='gray', highlightthickness=1)
    self._oper_actions_frame.columnconfigure(0, weight=1)
    self._oper_actions_frame.columnconfigure(1, weight=1)
    self._oper_actions_frame.columnconfigure(2, weight=1)
    self._oper_actions_frame.columnconfigure(3, weight=1)
    self._oper_actions_frame.columnconfigure(4, weight=1)
    self._oper_actions_frame.grid_propagate(False)
 
    self.btn_add = Button(self._oper_actions_frame, text='Add', width=BTNW_S)
    self.btn_remove = Button(self._oper_actions_frame, text='Remove', width=BTNW_S)
    self.btn_reset = Button(self._oper_actions_frame, text='Reset', width=BTNW_S)
    self.btn_save = Button(self._oper_actions_frame, text='Save', width=BTNW_S)
    self.btn_empty = Label(self._oper_actions_frame, width=BTNW_S)

    self.btn_add.grid(row=0, column=0, padx=PADX, pady=PADY_S, sticky=W)   
    self.btn_remove.grid(row=0, column=1, padx=PADX, pady=PADY_S, sticky=W)
    self.btn_reset.grid(row=0, column=2, padx=PADX, pady=PADY_S, sticky=W)
    self.btn_empty.grid(row=0, column=3, padx=PADX, pady=PADY_S, sticky=W)
    self.btn_save.grid(row=0, column=4, padx=PADX, pady=PADY_S, sticky=E)
    return

  def  _setup_flow_actions_view(self) -> None:
    # Setup flow actions view
    fr_h = int(self._h*0.11)
    self._flow_actions_frame = Frame(self, height=fr_h, highlightbackground='gray', highlightthickness=1)
    self._flow_actions_frame.columnconfigure(0, weight=1)
    self._flow_actions_frame.columnconfigure(1, weight=1)
    self._flow_actions_frame.columnconfigure(2, weight=1)
    self._flow_actions_frame.columnconfigure(3, weight=1)
    self._flow_actions_frame.columnconfigure(4, weight=1)
    self._flow_actions_frame.grid_propagate(False)
    self.btn_run = Button(self._flow_actions_frame, text='Run', width=BTNW_S)
    self.btn_curr = Button(self._flow_actions_frame, text='Current', width=BTNW_S)
    self.btn_next = Button(self._flow_actions_frame, text='Next', width=BTNW_S)
    self.btn_prev = Button(self._flow_actions_frame, text='Prev', width=BTNW_S)
    self.btn_top = Button(self._flow_actions_frame, text='Top', width=BTNW_S)

    self.btn_run.grid(row=0, column=0, padx=PADX, pady=PADY_S, sticky=W)
    self.btn_curr.grid(row=0, column=1, padx=PADX, pady=PADY_S, sticky=W)
    self.btn_next.grid(row=0, column=2, padx=PADX, pady=PADY_S, sticky=W)
    self.btn_prev.grid(row=0, column=3, padx=PADX, pady=PADY_S, sticky=W)
    self.btn_top.grid(row=0, column=4, padx=PADX, pady=PADY_S, sticky=W)
    return

  def _setup_views_layout(self) -> None:
    # Setup widgets groups layout
    self._flow_names_frame.grid(row=0, column=0, columnspan=2, padx=PADX, pady=PADY_S, sticky=W+E+N+S)
    self._flow_items_frame.grid(row=1, column=0, columnspan=2, padx=PADX, pady=PADY_S, sticky=W+E+N+S)   
    self._oper_actions_frame.grid(row=2, column=0, columnspan=2, padx=PADX, pady=PADY_S, sticky=W+E+N+S)
    self._flow_actions_frame.grid(row=3, column=0, columnspan=2, padx=PADX, pady=PADY_S, sticky=W+E+N+S)
    return

# Interfaces
  def clear_flow_tree_view(self):
    items = self.flow_tree_view.get_children()
    for item in items:
      self.flow_tree_view.delete(item)
    return
    
  def set_flow_item_names(self, flow_names, flow_titles, idx=0):
    self.clear_flow_tree_view()
    for i, name in enumerate(flow_names):
      idx_s = f'{i:02}'
      if flow_titles[i] == '':
        flow_titles[i] = idx_s
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
    if cur_item == '':
      return (0, '')
    item = self.flow_tree_view.item(cur_item)  
    return (idx, item.get('values')[0])
  
  @property
  def ws_names(self) -> List[str]:
    return self.names_combo_box.get('values')

  @ws_names.setter
  def ws_names(self, ws_names: List[str]) ->None:
    self.names_combo_box['values'] = ws_names
    self.names_combo_box.current(0)
    return

  def activate_edit_buttons(self, activate=False) -> None:
    state = DISABLED
    if activate:
      state = NORMAL
    self.btn_add['state']=state
    self.btn_remove['state']=state
    self.btn_reset['state']=state
    self.btn_save['state']=state
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
    self.activate_runtime_buttons(activate)
    return
