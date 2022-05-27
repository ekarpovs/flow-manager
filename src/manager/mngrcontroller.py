from tkinter import *
from tkinter.ttk import Combobox, Spinbox, Button
from typing import Callable, Dict, List, Tuple
import cv2
import copy
import os
from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfilename

from flow_storage import *
from flow_model import FlowItemModel, FlowItemType

from .mngrmodel import MngrModel  
from .mngrrunner import MngrRunner 
from .mngrconverter import MngrConverter  
from .mngrview import MngrView  
from .views.paramsview import convert_params_def_to_dict
from ..configuration import Configuration

class MngrController():
  def __init__(self, parent):
    self._parent = parent
    self._cfg = Configuration()
    self._model = MngrModel(self._cfg)
    self._runner = MngrRunner(self._cfg)
    self._converter = MngrConverter()
    self._view = MngrView(parent)
    # Bind to modules panel
    self._view.module.tree_view.bind('<<TreeviewOpen>>', self._open_all)
    self._view.module.tree_view.bind('<<TreeviewSelect>>', self._module_tree_selection_changed)
    # Bind to flows panel
    self.flows_view_idx = 0  
    self._view.flow.names_combo_box.bind('<<ComboboxSelected>>', self._worksheet_selected)
    self._view.flow.btn_reload.bind("<Button>", self._reload_ws_list)
    
    self._view.flow.btn_add.configure(command=self._add_operation_to_flow_model)
    self._view.flow.btn_remove.configure(command=self._remove_operation_from_flow_model)
    self._view.flow.btn_reset.configure(command=self._reset_flow_model)
    self._view.flow.btn_save.configure(command=self._store_flow_model_as_ws)
    # self._view.flow.btn_links.configure(command=self._edit_flow_links)
    
    self._view.flow.btn_run.configure(command=self._run)   
    self._view.flow.btn_curr.configure(command=self._apply)   
    self._view.flow.btn_next.configure(command=self._next)
    self._view.flow.btn_prev.configure(command=self._prev)
    self._view.flow.btn_top.configure(command=self._top)

    self._view.flow.flow_tree_view.bind('<<TreeviewSelect>>', self._tree_selection_changed)

    self._view.params.btn_params_reset.configure(command=self._reset)
    self._view.params.btn_params_default.configure(command=self._default) 
    self._view.params.btn_params_io.configure(command=self._get_io_object) 

    self._start()
    return


# Initialization
  def _start(self) -> None:
    self._update_module_view()
    self._update_worksheet_list()
    self._set_top_state()
    return

  def _update_module_view(self) -> None:   
    module_defs = self._converter.modulelist_to_module_defs(self._model.module)
    self._view.module_defs = module_defs
    return

  def _update_worksheet_list(self) -> None:
    names = self._model.flow.worksheetnames
    names.sort()
    names.insert(0, 'new <>')
    self._view.ws_names = names
    return


# Modules panel' events
  def _open_all(self, event) -> None:
    self._view.module.open_all()
    return

  def _module_tree_selection_changed(self, event) -> None:
    name = self._view.module.get_current_selection_tree()
    doc = ''
    if name != '':
      operation = self._model.module.get_operation_by_name(name)
      doc = operation._doc
    self._view.module.set_operation_doc(doc)
    return

# Flows panel's events
  def _worksheet_selected(self, event) -> None:
    ws_name = self._view.flow.names_combo_box.get()
    self._init_flow_model(ws_name)
    self._view.ws_title = self._model.flow.flow.info
    return

  # When a worksheet item is selected
  def _init_flow_model(self, ws_name: str) -> None:
    self._clear_logs()
    (ws_path, ws_name) = self._converter.split_ws_name(ws_name)
    # Create current flow model regarding ws defintion
    self._model.init_flow_model(ws_path, ws_name)
    names, titles = self._model.flow.get_names()
    self._view.flow.set_flow_item_names(names, titles)   
    self._update_flow_by_operations_definitions(names)
    # self._init_flow_output_refs(names) 
    self._rebuild_runner()
    return

  def _clear_logs(self) -> None:
    children = self._parent.master.children
    actions_frame = children['!mainactions']
    actions_frame.clear()
    return

  def _unbind_item_params_widgets(self) -> None:
    widgets = self._view.params.get_active_item_params_widgets()
    for widget in widgets:
      t = type(widget) 
      if t == Scale: 
        widget.unbind("<ButtonRelease-1>")
      elif t == Spinbox:
        widget.unbind("<ButtonRelease-1>")
      elif t == Checkbutton:
        widget.configure(command=None)
      elif t == Combobox:
        widget.unbind("<<ComboboxSelected>>")
      elif t == Entry:
        widget.unbind("<Return>")
      else:
        pass
    return

  def _bind_item_params_widgets(self) -> None:
    widgets = self._view.params.get_active_item_params_widgets()
    for widget in widgets:
      t = type(widget) 
      if t == Scale: 
        widget.bind("<ButtonRelease-1>", self._apply)
      elif t == Spinbox:
        widget.bind("<ButtonRelease-1>", self._apply)
      elif t == Checkbutton:
        widget.configure(command=self._apply)
      elif t == Combobox:
        widget.bind("<<ComboboxSelected>>", self._apply)
      elif t == Entry:
        widget.bind("<Return>", self._params_return_pressed)
      else:
        pass
    return

  def _activate_item_params(self, idx: int = 0) -> None:
    self._view.params.set_active_wd(idx)
    self._bind_item_params_widgets()
    return

  def _activate_item_links(self, idx: int = 0) -> None:
    self._view.links.set_active_wd(idx)
    self._bind_item_links_widgets()
    return

  def _tree_selection_changed(self, event) -> None:
    idx, name = self._view.flow.get_current_selection_tree()
    if self._model.flow.flow is not None:
      self._activate_item_params(idx)
      self._activate_item_links(idx)
    return

  def _assign_operation_definitions(self, name: str, item: FlowItemModel) -> None:
    operation = self._model.module.get_operation_by_name(name)
    item.params_def = operation.params
    item.inrefs_def = operation.inrefs
    item.outrefs_def = operation.outrefs
    return

  def _update_flow_by_operations_definitions(self, names: List[str]) -> None:
    for idx, name in enumerate(names):
      item = self._model.flow.get_item(idx)
      self._assign_operation_definitions(name, item)
    return 


# Flows panel's commands 
  def _reload_ws_list(self, event) -> None:
    self._model.flow.reload()
    names = self._model.flow.worksheetnames
    names.insert(0, 'new <>')
    self._view.ws_names = names
    # self._view.ws_title = self._model.flow.flow.info
    if event is not None:
      # don't clear after store ws
      self._view.flow.clear_flow_tree_view()
      self._view.data.clear_view()
      self._view.ws_title = ''
      self._view.params.clear()
      self._view.links.clear()
    return

  def _add_operation_to_flow_model(self) -> None:
    # Get destination item position before that will be added new one
    cur_idx, _ = self._view.flow.get_current_selection_tree()
    cur_idx = max(1, cur_idx)
    # Get source item position from modules view
    name = self._view.module.get_selected_item_name()   
    # Perform if operation only selected
    if name is not None:     
      new_flow_item = FlowItemModel(FlowItemType.EXEC, name)
      self._assign_operation_definitions(name, new_flow_item)
      self._model.flow.set_item(cur_idx, new_flow_item)
      names, titles = self._model.flow.get_names()
      self._view.flow.set_flow_item_names(names, titles)   
      # self._init_flow_output_refs(names)
      self._rebuild_runner()
    return

  def _remove_operation_from_flow_model(self) -> None:
    cur_idx, _ = self._view.flow.get_current_selection_tree()
    if cur_idx == 0 or cur_idx == len(self._model.flow.items) -1:
      return
    self._model.flow.remove_item(cur_idx)
    names, titles = self._model.flow.get_names()
    self._view.flow.set_flow_item_names(names, titles)
    # self._init_flow_output_refs(names)
    self._rebuild_runner()
    return

  def _reset_flow_model(self) -> None:
    ws_name = self._view.flow.names_combo_box.get()
    self._init_flow_model(ws_name)
    self._current()
    return
  
  def _store_flow_model_as_ws(self) -> None:
    flow_name = self._view.flow.names_combo_box.get()
    path, name = self._converter.flow.split_ws_name(flow_name)
    (new_path, stored_as) = self._model.flow.store_flow_model_as_ws(path, name)
    # TODO: implement change flow name and reload? 
    ws_name = f'{stored_as} <{new_path}>'
    # self._reload_ws_list(None)
    self._view.flow.names_combo_box.set(ws_name)
    return

  def _update_flow(self) -> None:
    names, titles = self._model.flow.get_names()
    self._view.flow.set_flow_item_names(names, titles)   
    self._view.ws_title = self._model.flow.flow.info
    self._rebuild_runner()
    return 

  def _apply_step_params(self, idx: int) -> None:
    flow_item = self._model.flow.get_item(idx)
    params_wd = self._view.params.get_item_params(idx)
    for k in params_wd.keys():
      flow_item.params[k] = params_wd.get(k)
    return

  def _reset_step_params(self, idx: int) -> None:
    flow_item = self._model.flow.get_item(idx)
    params_ws = flow_item.params_ws
    params_def = flow_item.params_def
    params = {} 
    for param_def in params_def:
      k = param_def.get('name')
      param_new_val = params_ws.get(k)
      if param_new_val is None:
        # use default value from def
        param_new_val = param_def.get('default')
      flow_item.params[k] = param_new_val
      params[k] = param_new_val
    self._view.params.set_item_params(idx, params)
    return

  def _default_step_params(self, idx: int) -> None:
    flow_item = self._model.flow.get_item(idx)
    params_def = flow_item.params_def
    params = convert_params_def_to_dict(params_def)    
    flow_item.params = params
    self._view.params.set_item_params(idx, params)
    return

# Execution commands
  def _show_step_result(self, idx: int) -> None:
    state_id = self._runner.output_from_state
    self._view.data.show_preview_result(state_id, idx)
    return

  def _show_run_result(self) -> None:
    state_id = self._runner.output_from_state   
    self._view.data.show_result(state_id)
    return


  def _clear_step_result(self, idx: int) -> None:
    state_id = self._runner.state_id
    self._view.data.update_result(idx, state_id)
    return

  def _run(self) -> None:
    idx = self._runner.state_idx
    if self._ready():
      self._runner.run_all(self._model.flow.flow)
      idx = self._runner.state_idx
      self._view.flow.set_selection_tree(idx)
      self._show_run_result()
    return

  def _step(self, event_name: str) -> None:
    if self._ready():
      idx, _ = self._view.flow.get_current_selection_tree()
      self._apply_step_params(idx)
      self._runner.run_one(event_name, idx, self._model.flow.flow)
      new_idx = self._runner.state_idx
      self._view.flow.set_selection_tree(new_idx)
    return

  def _next(self)  -> None:
    self._view.data.default()
    idx, _ = self._view.flow.get_current_selection_tree()
    if self._ready() and self._runner.state_idx == idx:
      self._step('next')
      self._show_step_result(idx)
    else:
      self._set_top_state()
    return 

  def _current(self) -> None:
    self._step('current')
    idx, _ = self._view.flow.get_current_selection_tree()
    self._show_step_result(idx)
    return 

  def _prev(self) -> None:
    self._unbind_item_links_widgets()
    self._unbind_item_params_widgets()
    self._step('prev')
    idx = self._runner.state_idx
    self._clear_step_result(idx)
    return 

  def _top(self) -> None:
    self._set_top_state()
    return
  
  def _set_top_state(self) -> None:
    self._view.data.clear_view()
    self._view.flow.set_selection_tree()
    if self._ready():
      # self._view.flow.set_selection_tree()
      self._runner.reset()
    return

  def _run_current(self, idx: int) -> None:
    if self._ready() and self._runner.state_idx == idx:
      self._current()
    return

# Links view
  def _flow_title_return_pressed(self, getter: Callable) -> None:
    self._model.flow.flow.info = copy.copy(getter())
    return

  
  def _links_return_pressed(self, getter: Callable) -> None:
    idx, _ = self._view.flow.get_current_selection_tree()
    flow_item = self._model.flow.get_item(idx)
    flow_item.title = copy.copy(getter())
    return


  def _unbind_item_links_widgets(self) -> None:
    descriptors = self._view.links.get_active_item_link_descriptors()
    for descr in descriptors:
      widget = descr.get('wd')
      t = type(widget)
      if t == Combobox:
        widget.unbind("<<ComboboxSelected>>")
      elif t == Entry:
        widget.unbind("<Return>")
      else:
        pass
    return

  def _bind_item_links_widgets(self) -> None:
    descriptors = self._view.links.get_active_item_link_descriptors()
    for descr in descriptors:
      widget = descr.get('wd')
      t = type(widget)
      if t == Combobox:
        name = descr.get('name')
        cgetter = descr.get('getter')
        widget.bind("<<ComboboxSelected>>", lambda e: self._assign_link(name, cgetter))
      elif t == Entry:
        egetter = descr.get('getter')
        widget.bind("<Return>", lambda e: self._links_return_pressed(egetter))
      else:
        pass
    return

  def _assign_link(self, name: str, getter: Callable) -> None:
    idx, _ = self._view.flow.get_current_selection_tree()
    # set active 
    flow_item = self._model.flow.get_item(idx)
    ext_ref = copy.copy(getter())
    flow_item.links[name] = ext_ref
    # Update sorage
    storage_in_ref = self._runner.storage.get_state_input_ext_ref(self._runner.state_id, name)
    storage_in_ref.ext_ref = ext_ref
    self._apply()
    return

  def _params_return_pressed(self, event) -> None:
    self._apply(event)
    return

  def _get_changed_param_widget_idx(self, event: Event) -> int:
    idx = 100
    widget: Widget = getattr(event, 'widget', None)
    if widget is not None:
      parent_full_name = widget.winfo_parent()
      parent_name = parent_full_name[parent_full_name.index('--'):]
      idx_s = parent_name[2:4]
      if not idx_s.isnumeric():
        idx_s = idx_s[0:1]
      idx = int(idx_s)
    return idx

  def _apply(self, event=None) -> None:
    idx, _ = self._view.flow.get_current_selection_tree()
    par_idx = self._get_changed_param_widget_idx(event)
    if idx > par_idx:
      # go backward and forwarrd with new param value
      for i in range(idx - par_idx):
        self._prev()
      for i in range(idx - par_idx):
        self._next()
    self._run_current(idx)
    return

  def _reset(self) -> None:
    idx, _ = self._view.flow.get_current_selection_tree()
    self._reset_step_params(idx)
    self._run_current(idx)
    return

  def _default(self) -> None:
    idx, _ = self._view.flow.get_current_selection_tree()
    self._default_step_params(idx)
    self._run_current(idx)
    return

# Runner
  def _ready(self) -> bool:
    activate = self._runner.initialized and self._model.flow.loaded
    self._view.flow.activate_buttons(activate)
    return activate

  def _create_and_activate_links_view(self) -> None:
    self._view.links.build(self._model.flow.flow)
    info_descr = self._view.links.info_descr
    widget = info_descr.get('wd')
    getter = info_descr.get('getter')
    widget.bind("<Return>", lambda e: self._flow_title_return_pressed(getter))
    self._activate_item_links()      
    return

  def _create_and_activate_params_view(self) -> None:
    self._view.params.build(self._model.flow.flow)
    self._activate_item_params()
    return

  def _rebuild_runner(self) -> None:
    self._view.params.clear()
    self._view.links.clear()
    if self._model.flow:
      self._create_and_activate_links_view()
      self._create_and_activate_params_view()
      self._runner.build(self._model.flow.flow)
      # for plotting
      self._view.data.storage = self._runner.storage
    self._set_top_state()
    return


# Data commands
  @staticmethod
  def _set_data_location_to_params(io_obj: str, params: Dict, key: str) -> None:
    if '.' in io_obj: 
      path, name = os.path.split(io_obj)
    else:
      path = io_obj
      name = ''
    params['path'] = path
    if key == 'src':
      params['src'] = name
    else:
      params['dest'] = name
    return

  def _assign_location(self, idx: int, name: str, io_obj:str, key: str) -> None:
    flow_item = self._model.flow.get_item(idx)
    params_def = flow_item.params_def   
    params = flow_item.params
    p = [p for p in params_def if p.get('name') == 'path' or p.get('name') == 'src' or p.get('name') == 'dest']
    if p is not None:
      self._set_data_location_to_params(io_obj, params, key)
    self._view.params.set_item_params(idx, params)
    self._apply(None)
    return
  
  def _get_io_object(self) -> None:
    init_dir = self._cfg.input_paths
    idx, name = self._view.flow.get_current_selection_tree()
    flow_item = self._model.flow.get_item(idx)
    params_def = flow_item.params_def
    io_obj = ''
    full = False
    key = ''
    for p_def in params_def:
      key = p_def.get('name')
      if key == 'src' or key == 'dest':
        full = True
        break;
    if full and key == 'src':
      io_obj = self._get_full_file_name(init_dir)
    elif full and key == 'dest':
      io_obj = self._store_to(init_dir)
    else:
      io_obj = self._get_directory(init_dir)
    if io_obj != '':
      self._assign_location(idx, name, io_obj, key)
    return

  def _get_directory(self, init_dir: str) -> str:
    dir = askdirectory(initialdir=init_dir)
    return dir

  def _get_full_file_name(self, init_dir: str) -> str:
    ffn = askopenfilename(initialdir=init_dir, title="Select a file", filetypes=self._file_types)
    return ffn

  def _store_to(self, init_dir: str) -> str:
    ffn = asksaveasfilename(initialdir = init_dir, initialfile = '', defaultextension=".tiff", filetypes=self._file_types)
    return ffn

  @property
  def _file_types(self) -> str:
    return (("image files","*.png"), 
            ("image files","*.jpeg"), 
            ("image files","*.jpg"), 
            ("image files","*.tiff"), 
            ("json files","*.json"), 
            ("all files","*.*"))
