from tkinter import *
from tkinter.ttk import Combobox, Spinbox, Button
from typing import Dict, List, Tuple
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
from ..configuration import Configuration

class MngrController():
  def __init__(self, parent):
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
    self._view.flow.btn_links.configure(command=self._edit_flow_links)
    
    self._view.flow.btn_run.configure(command=self._run)   
    self._view.flow.btn_curr.configure(command=self._apply)   
    self._view.flow.btn_next.configure(command=self._next)
    self._view.flow.btn_prev.configure(command=self._prev)
    self._view.flow.btn_top.configure(command=self._top)

    self._view.flow.flow_tree_view.bind('<<TreeviewSelect>>', self._tree_selection_changed)

    self._view.flow.btn_params_reset.configure(command=self._reset)
    self._view.flow.btn_params_default.configure(command=self._default) 
    self._view.flow.btn_params_io.configure(command=self._get_io_object) 

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
    return

  # When a worksheet item is selected
  def _init_flow_model(self, ws_name: str) -> None:
    (ws_path, ws_name) = self._converter.split_ws_name(ws_name)
    # Create current flow model regarding ws defintion
    self._model.init_flow_model(ws_path, ws_name)
    names = self._model.flow.get_names()
    self._view.flow.set_flow_item_names(names)   
    self._update_flow_by_operations_params_def(names)
    self._create_current_operation_params_controls(0, names[0])
    self._rebuild_runner()
    return

  def _tree_selection_changed(self, event) -> None:
    idx, name = self._view.flow.get_current_selection_tree()
    controls_idx = self._view.flow.get_current_opreation_params_idx()
    if controls_idx == -1 or controls_idx != idx:
      self._create_current_operation_params_controls(idx, name)
    return

  def _assign_oper_params(self, name: str, item: FlowItemModel) -> None:
    operation = self._model.module.get_operation_by_name(name)
    item.params_def = operation.params
    return

  def _update_flow_by_operations_params_def(self, names: List[str]) -> None:
    for idx, name in enumerate(names):
      item = self._model.flow.get_item(idx)
      self._assign_oper_params(name, item)
    return 


# Flows panel's commands 
  def _reload_ws_list(self, event) -> None:
    self._model.flow.reload()
    names = self._model.flow.worksheetnames
    names.insert(0, 'new <>')
    self._view.ws_names = names
    if event is not None:
      # don't clear after store ws
      self._view.flow.clear_flow_tree_view()
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
      self._assign_oper_params(name, new_flow_item)
      self._model.flow.set_item(cur_idx, new_flow_item)
      names = self._model.flow.get_names()
      self._view.flow.set_flow_item_names(names)   
      self._rebuild_runner()
    return

  def _remove_operation_from_flow_model(self) -> None:
    cur_idx, _ = self._view.flow.get_current_selection_tree()
    if cur_idx == 0 or cur_idx == len(self._model.flow.items) -1:
      return
    self._model.flow.remove_item(cur_idx)
    names = self._model.flow.get_names()
    self._view.flow.set_flow_item_names(names)   
    self._rebuild_runner()
    return

  def _reset_flow_model(self) -> None:
    ws_name = self._view.flow.names_combo_box.get()
    self._init_flow_model(ws_name)
    self._rebuild_runner()
    return

  def _store_flow_model_as_ws(self) -> None:
    flow_name = self._view.flow.names_combo_box.get()
    path, name = self._converter.flow.split_ws_name(flow_name)
    (new_path, stored_as) = self._model.flow.store_flow_model_as_ws(path, name)
    # TODO: implement change flow name and reload? 
    ws_name = f'{stored_as} <{new_path}>'
    self._reload_ws_list(None)
    self._view.flow.names_combo_box.set(ws_name)
    return

  def _edit_flow_links(self) -> None:
    self._view.flow.edit_flow_links(self._model.flow, self._rebuild_runner)
    return


# Execution commands
  def _set_step_result(self) -> None:
    out = self._runner.get_current_output()
    self._view.data.set_preview(out)
    return

  def _clear_step_result(self) -> None:
    idx = self._runner.state_idx
    self._view.data.clear_preview(idx)
    return

  def _run(self) -> None:
    idx = self._runner.state_idx
    if self._ready():
      self._runner.run_all(self._model.flow.flow)
      idx = self._runner.state_idx
      self._view.flow.set_selection_tree(idx)
    return

  def _step(self, event_name: str) -> None:
    if self._ready():
      idx, _ = self._view.flow.get_current_selection_tree()
      self._runner.run_one(event_name, idx, self._model.flow.flow)
      new_idx = self._runner.state_idx
      self._view.flow.set_selection_tree(new_idx)
    return

  def _next(self)  -> int:
    self._step('next')
    self._set_step_result()
    return 

  def _current(self) -> int:
    self._step('current')
    self._set_step_result()
    return 

  def _prev(self) -> int:
    self._step('prev')
    self._clear_step_result()
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


# Operation parameters sub panel's commands
  def _bind_param_controls(self, params_def) -> None:
    for param_def in params_def:
      cname = param_def.get('name')
      ctype = param_def.get('type')
      param_control = self._view.flow.get_current_operation_param_control(cname)
      t = type(param_control) 
      if t == Scale: 
        param_control.bind("<ButtonRelease-1>", self._apply)
      elif t == Spinbox:
        param_control.bind("<ButtonRelease-1>", self._apply)
      elif t == Checkbutton:
        param_control.configure(command=self._apply)
      elif t == Combobox:
        param_control.bind("<<ComboboxSelected>>", self._apply)
      elif t == Entry:
        param_control.bind("<Key>", self._key_pressed)
      else:
        pass
    return

  def _create_current_operation_params_controls(self, idx, name) -> None:
    flow_item = self._model.flow.get_item(idx)
    params_def = flow_item.params_def
    # merge curent params and params_ws
    params = flow_item.params
    params_ws = flow_item.params_ws
    for k in params_ws.keys():
      if k in params:
        continue
      params[k] = params_ws.ket(k)
    self._view.flow.create_operation_params_controls(idx, name, params, copy.deepcopy(params_def))
    self._bind_param_controls(params_def)
    self._view.flow.btn_params_io['state'] = DISABLED
    if 'path' in params:
      self._view.flow.btn_params_io['state'] = NORMAL
    return

  def _key_pressed(self, event) -> None:
    if event.keycode == 13:
      self._apply()
    return

  def _apply(self, event=None) -> None:
    idx, name = self._view.flow.get_current_selection_tree()
    flow_item = self._model.flow.get_item(idx)
    params_new = self._view.flow.get_current_operation_params_def()
    for k in params_new.keys():
      flow_item.params[k] = params_new.get(k)
    self._run_current(idx)
    return

  def _reset(self) -> None:
    idx, name = self._view.flow.get_current_selection_tree()
    flow_item = self._model.flow.get_item(idx)
    params_def = flow_item.params_def   
    params = copy.deepcopy(flow_item.params_ws)
    flow_item.params = params
    self._view.flow.create_operation_params_controls(idx, name, params, copy.deepcopy(params_def))
    self._bind_param_controls(params_def)

    self._run_current(idx)
    return

  def _default(self) -> None:
    idx, name = self._view.flow.get_current_selection_tree()
    flow_item = self._model.flow.get_item(idx)
    params_def = flow_item.params_def   
    params = self._converter.flow.convert_params_def_to_dict(flow_item.params_def)
    flow_item.params = params
    self._view.flow.create_operation_params_controls(idx, name, params, copy.deepcopy(params_def))
    self._bind_param_controls(params_def)

    self._run_current(idx)
    return

# Runner
  def _ready(self) -> bool:
    activate = self._runner.initialized and self._model.flow.loaded
    self._view.flow.activate_buttons(activate)
    return activate

  def _rebuild_runner(self) -> None:
    if self._model.flow:
      self._runner.build(self._model.flow.flow)
      # for plotting
      self._view.data.storage = self._runner.storage
    self._set_top_state()
    return


# Data commands
  @staticmethod
  def _set_image_location_to_params(io_obj: str, params: Dict) -> None:
    if '.' in io_obj: 
      path, name = os.path.split(io_obj)
    else:
      path = io_obj
      name = ''
    params['path'] = path
    params['name'] = name
    return

  def _assign_location(self, idx: int, name: str, io_obj:str) -> None:
    flow_item = self._model.flow.get_item(idx)
    params_def = flow_item.params_def   
    params = flow_item.params

    p = [p for p in params_def if p.get('name') == 'path' or p.get('name') == 'name']
    if p is not None:
      self._set_image_location_to_params(io_obj, params)
    self._view.flow.create_operation_params_controls(idx, name, params, copy.deepcopy(params_def))
    self._bind_param_controls(params_def)
    self._apply(None)
    return
  
  def _get_io_object(self) -> None:
    init_dir = self._cfg.input_paths
    idx, name = self._view.flow.get_current_selection_tree()
    flow_item = self._model.flow.get_item(idx)
    params_def = flow_item.params_def
    io_obj = ''
    full = False
    for p_def in params_def:
      if p_def.get('name') == 'name':
        full = True
        break;
    if full:
      io_obj = self._get_full_file_name(init_dir)
      # io_obj = self._store_to(init_dir)
    else:
      io_obj = self._get_directory(init_dir)
    if io_obj != '':
      self._assign_location(idx, name, io_obj)
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
