from tkinter import *
from tkinter.ttk import Combobox
from typing import Dict, List, Tuple
import cv2
import copy
import os
from tkinter.filedialog import askopenfilename

from flow_storage import FlowDataType
from flow_model import FlowItemModel, FlowItemType

from .mngrmodel import MngrModel  
from .mngrrunner import MngrRunner 
from .mngrconverter import MngrConverter  
from .mngrview import MngrView  
from ..configuration import Configuration

class MngrController():
  def __init__(self, parent):
    self.cfg = Configuration()
    self._model = MngrModel(self.cfg)
    self._runner = MngrRunner(self.cfg)
    self._converter = MngrConverter()
    self._view = MngrView(parent)
    # Bind to modules panel
    self._view.module.tree_view.bind('<<TreeviewOpen>>', self._open_all)
    self._view.module.tree_view.bind('<<TreeviewSelect>>', self._module_tree_selection_changed)
    # Bind to flows panel
    self.flows_view_idx = 0  
    self._view.flow.names_combo_box.bind('<<ComboboxSelected>>', self._worksheet_selected)
    self._view.flow.btn_reload.bind("<Button>", self._reload_ws_list)
    self._view.flow.btn_add.bind("<Button>", self._add_operation_to_flow_model)
    self._view.flow.btn_remove.bind("<Button>", self._remove_operation_from_flow_model)
    self._view.flow.btn_reset.bind("<Button>", self._reset_flow_model)
    self._view.flow.btn_save.bind("<Button>", self._store_flow_model_as_ws)
    self._view.flow.btn_links.bind("<Button>", self._edit_flow_links)
    self._view.flow.btn_run.bind("<Button>", self._run)
    self._view.flow.btn_next.bind("<Button>", self._next)
    self._view.flow.btn_prev.bind("<Button>", self._prev)
    self._view.flow.btn_top.bind("<Button>", self._top)
    self._view.flow.flow_tree_view.bind('<<TreeviewSelect>>', self._tree_selection_changed)
    self._view.flow.btn_params_apply.bind("<Button>", self._apply)
    self._view.flow.btn_params_reset.bind("<Button>", self._reset)
    self._view.flow.btn_params_default.bind("<Button>", self._default)

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
    if name is not '':
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
    self._view.flow.activate_buttons()
    (ws_path, ws_name) = self._converter.split_ws_name(ws_name)
    # Create current flow model regarding ws defintion
    self._model.init_flow_model(ws_path, ws_name)
    names = self._model.flow.get_names()
    self._view.flow.set_flow_item_names(names)   
    self._update_flow_by_operations_params_def(names)
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
    item.inrefs_def = operation.inrefs
    item.outrefs_def = operation.outrefs
    return

  def _update_flow_by_operations_params_def(self, names: List[str]) -> None:
    for idx, name in enumerate(names):
      item = self._model.flow.get_item(idx)
      self._assign_oper_params(name, item)
      # operation = self._model.module.get_operation_by_name(name)
      # item.params_def = operation.params
      # item.inrefs_def = operation.inrefs
      # item.outrefs_def = operation.outrefs
    return 


# Flows panel's commands 
  def _reload_ws_list(self, event) -> None:
    self._model.flow.reload()
    names = self._model.flow.worksheetnames
    names.insert(0, 'new <>')
    self._view.ws_names = names
    return

  def _add_operation_to_flow_model(self, event) -> None:
    # Get destination item position before that will be added new one
    cur_idx, _ = self._view.flow.get_current_selection_tree()
    cur_idx = max(1, cur_idx)
    # Get source item position from modules view
    name = self._view.module.get_selected_item_name()   
    # Perform if operation only selected
    if name is not None:     
      new_flow_item = FlowItemModel(FlowItemType.EXEC, name)
      self._assign_oper_params(name, new_flow_item)
      # operation = self._model.module.get_operation_by_name(name)
      # new_flow_tem.params_def = operation.params
      # new_flow_tem.inrefs_def = operation.inrefs
      # new_flow_tem.outrefs_def = operation.outrefs
      self._model.flow.set_item(cur_idx, new_flow_item)
      names = self._model.flow.get_names()
      self._view.flow.set_flow_item_names(names)   
      self._rebuild_runner()
    return

  def _remove_operation_from_flow_model(self, event) -> None:
    cur_idx, _ = self._view.flow.get_current_selection_tree()
    if cur_idx == 0 or cur_idx == len(self._model.flow.items) -1:
      return
    self._model.flow.remove_item(cur_idx)
    names = self._model.flow.get_names()
    self._view.flow.set_flow_item_names(names)   
    self._rebuild_runner()
    return

  def _reset_flow_model(self, event) -> None:
    ws_name = self._view.flow.names_combo_box.get()
    self._init_flow_model(ws_name)
    self._rebuild_runner()
    return

  def _store_flow_model_as_ws(self, event) -> None:
    flow_name = self._view.flow.names_combo_box.get()
    path, name = self._converter.flow.split_ws_name(flow_name)
    (new_path, stored_as) = self._model.flow.store_flow_model_as_ws(path, name)
    # TODO: implement change flow name and reload? 
    ws_name = f'{stored_as} <{new_path}>'
    self._reload_ws_list(None)
    self._view.flow.names_combo_box.set(ws_name)
    return

  def _edit_flow_links(self, event) -> None:
    self._view.flow.edit_flow_links(self._model.flow)
    return


# Execution commands
  def _set_result(self, idx: int, out: Tuple[List[Tuple[str, FlowDataType]], Dict] = None) -> None:
    if out is not None:
      out_refs, out_data = out
      for ref in out_refs:
        (ref_name, ref_type) = ref
        data = out_data[ref_name]
        if ref_type == FlowDataType.CV2_IMAGE:
          if data is not None:
            image = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
            self._view.data.set_result_image(image)
          else:  
            self._view.data.set_result_image(None)
        else:
          print(f'{ref_name}: ', data)
    else:
      self._view.data.set_result_image(None)
    self._view.flow.set_selection_tree(idx)
    return

  def _run(self, event) -> int:
    idx = self._runner.state_idx
    if self._ready():
      self._runner.run_all()
      idx = self._runner.state_idx
      out = self._runner.get_current_output()
      self._set_result(idx, out)
    return idx

  def _step(self, event_name: str) -> None:
    idx, _ = self._view.flow.get_current_selection_tree()
    if self._ready():
      self._runner.run_one(event_name, idx)
      idx = self._runner.state_idx
      out = self._runner.get_current_output()
      self._set_result(idx, out)
    return

  def _next(self, event)  -> int:
    self._step('next')

  def _current(self) -> int:
    return self._step('current')

  def _prev(self, event) -> int:
    return self._step('prev')

  def _top(self, event) -> None:
    self._set_top_state()
    return
  
  def _set_top_state(self) -> None:
    self._set_result(0)
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
      if ctype == 'button' and cname == 'define':
        param_control.bind("<Button>", self._get_path)
      else:
        t = type(param_control) 
        if t == Scale:
          param_control.bind("<ButtonRelease-1>", self._apply)
        elif t == Combobox:
          param_control.bind("<<ComboboxSelected>>", self._apply)          
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
    return

  def _apply(self, event) -> None:
    idx, name = self._view.flow.get_current_selection_tree()
    flow_item = self._model.flow.get_item(idx)
    params_new = self._view.flow.get_current_operation_params_def()
    for k in params_new.keys():
      flow_item.params[k] = params_new.get(k)

    self._run_current(idx)
    return

  def _reset(self, event) -> None:
    idx, name = self._view.flow.get_current_selection_tree()
    flow_item = self._model.flow.get_item(idx)
    params_def = flow_item.params_def   
    params = copy.deepcopy(flow_item.params_ws)
    flow_item.params = params
    self._view.flow.create_operation_params_controls(idx, name, params, copy.deepcopy(params_def))
    self._bind_param_controls(params_def)

    self._run_current(idx)
    return

  def _default(self, event) -> None:
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
    if self._runner.initialized and self._model.flow.loaded:
      self._view.flow.activate_buttons(True)
      return True
    else:
      self._view.flow.activate_buttons()
      return False

  def _rebuild_runner(self) -> None:
    if self._model.flow:
      self._runner.build(self._model.flow.flow)
    self._set_top_state()
    return

# Data commands
  @staticmethod
  def _set_image_location_to_params(ffn, params) -> None:
    path, name = os.path.split(ffn)
    params['path'] = path
    params['name'] = name
    return

  def _get_path(self, event) -> None:
    ffn = askopenfilename(title="Select a file", 
      filetypes=(("image files","*.png"), ("image files","*.jpeg"), ("image files","*.jpg"), ("image files","*.tiff"), ("all files","*.*")))
    if ffn is not '':
      idx, name = self._view.flow.get_current_selection_tree()
      flow_item = self._model.flow.get_item(idx)
      params_def = flow_item.params_def   
      params = flow_item.params

      p = [p for p in params_def if p.get('name') == 'path' or p.get('name') == 'name']
      if p is not None and len(p) == 2:
        self._set_image_location_to_params(ffn, params)
      self._view.flow.create_operation_params_controls(idx, name, params, copy.deepcopy(params_def))
      self._bind_param_controls(params_def)
      self._apply(None)
    return

