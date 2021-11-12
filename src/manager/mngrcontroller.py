from typing import Dict, List
import cv2
import numpy as np
import copy

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
# Bind to flows panel
    self.flows_view_idx = 0  
    self._view.flow.names_combo_box.bind('<<ComboboxSelected>>', self._worksheet_selected)
    self._view.flow.btn_add.bind("<Button>", self._add_operation_to_flow_model)
    self._view.flow.btn_remove.bind("<Button>", self._remove_operation_from_flow_model)
    self._view.flow.btn_reset.bind("<Button>", self._reset_flow_model)
    self._view.flow.btn_save.bind("<Button>", self._store_flow_model_as_ws)
    self._view.flow.btn_run.bind("<Button>", self._run)
    self._view.flow.btn_next.bind("<Button>", self._next)
    self._view.flow.btn_prev.bind("<Button>", self._prev)
    self._view.flow.btn_top.bind("<Button>", self._top)
    self._view.flow.oper_params_view.btn_apply.bind("<Button>", self._apply)
    self._view.flow.oper_params_view.btn_reset.bind("<Button>", self._reset)
    self._view.flow.flow_tree_view.bind('<<TreeviewSelect>>', self._tree_selection_changed)

# Bind to images panel
    # self._view.images_view.auto_input_check_button.bind('<<CheckbuttonChecked>>', lambda e: self.auto_input_changed(True))
    # self._view.images_view.auto_input_check_button.bind('<<CheckbuttonUnChecked>>', lambda e: self.auto_input_changed())
    self._view.image.btn_load.bind("<Button>", self._load)
    self._view.image.btn_clear.bind("<Button>", self._clear)
    self._view.image.names_combo_box.bind('<<ComboboxSelected>>', self._selected_path)  
    self._view.image.file_names_list_box.bind('<<ListboxSelect>>', 
      lambda e: self._image_file_selected(self._view.image.file_names_list_box.curselection()))

    self.file_idx = None
    self._start()


# Initialization
  def _start(self) -> None:
    self._update_module_view()
    self._update_worksheet_list()
    self._update_image_view()
    return

  def _update_module_view(self) -> None:   
    module_defs = self._converter.modulelist_to_module_defs(self._model.module)
    self._view.module_defs = module_defs
    return

  def _update_worksheet_list(self) -> None:
    names = self._model._worksheet.workseetnames
    names.insert(0, 'new <>')
    self._view.ws_names = names
    return

  def _update_image_view(self) -> None:
    self._view.image.set_input_paths(self.cfg.input_paths)
    return

# Actions
# Modules panel' events and commands
  def _open_all(self, event) -> None:
    self._view.module.open_all()
    return

# Flows panel's events and commands
  def _worksheet_selected(self, event) -> None:
    ws_name = self._view.flow.names_combo_box.get()
    self._init_flow_model(ws_name)
    return

  # When a worksheet item is selected
  def _init_flow_model(self, ws_name: str) -> None:
    self._view.flow.activate_buttons()
    (ws_path, ws_name) = self._converter.split_ws_name(ws_name)
    # Create current flow model regarding ws defintion
    self._model.create_flow_model(ws_path, ws_name)
    names = self._model.flow.get_names()
    self._view.flow.set_flow_item_names(names)   
    # Init the flow items models with default operations definitions
    self._set_operation_definitions(names)
    self._rebuild_runner()
    return


  def _tree_selection_changed(self, event) -> None:
    idx, item = self._view.flow.get_current_selection_tree()
    self._view.flow.clear_operation_params()
    name = item.get('text')
    item = self._model.flow.get_item(idx)
    self._set_operation_params(idx, name)
    return


# !!! Parameters 
  def _set_operation_definitions(self, names: List[str]) -> None:
    for idx, name in enumerate(names):
      operation = self._model.module.get_operation_by_name(name)
      item = self._model.flow.get_item(idx)
      item.params_def = operation.params
      item.inrefs_def = operation.inrefs
      item.outrefs_def = operation.outrefs
    return 


  def _set_operation_params(self, idx: int, operation_name: str) -> None:
    if self._model.flow is not None:
      item = self._model.flow.get_item(idx)
      # Merge default and current params
      params_def = item.params_def
      if len(params_def) == 0:
        return
      params_new = copy.deepcopy(params_def)
      params = item.params
      if params is not None:
        for param_new in params_new:
          pname_new = param_new.get('name')
          if pname_new in params:
            new_value = params.get(pname_new)
            param_new['default'] = new_value
        self._view.flow.set_operation_params(idx, operation_name, params_new)
    return

  def _add_operation_to_flow_model(self, event) -> None:
    # Get destination item position before that will be added new one
    cur_idx, item = self._view.flow.get_current_selection_tree()
    # Get source item position from modules view
    name = self._view.module.get_selected_item_name()   
    # Perform if operation only selected
    if name is not None:     
      new_flow_tem = FlowItemModel(FlowItemType.EXEC, name)
      operation = self._model.module.get_operation_by_name(name)
      new_flow_tem.params_def = operation.params
      self._model.flow.set_item(cur_idx, new_flow_tem)
      names = self._model.flow.get_names()
      self._view.flow.set_flow_item_names(names)   
      self._rebuild_runner()
    return

  def _remove_operation_from_flow_model(self, event) -> None:
    cur_idx, _ = self._view.flow.get_current_selection_tree()
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

  def _store_flow_model_as_ws(self, event):
    flow_name = self._view.flow.names_combo_box.get()
    path, name = self._converter.flow.split_ws_name(flow_name)
    return

# Execution commands
  def _set_result(self, idx: int, data: Dict) -> None:
    cv2image = data.get('image')
    if cv2image is not None:
      cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGB)
    # if cv2image is not None:
    self._view.image.set_result_image(cv2image)
    self._view.flow.set_selection_tree(idx)
    return

  def _run(self, event) -> int:
    idx = self._runner.state_idx
    if self._ready():
      self._runner.run_all()
      idx = self._runner.state_idx
      data = self._runner.get_current_output()
      self._set_result(idx, data)
    return idx

  def _step(self, event_name: str) -> None:
    idx, _ = self._view.flow.get_current_selection_tree()
    if self._ready():
      self._runner.run_one(event_name, idx)
      idx = self._runner.state_idx
      data = self._runner.get_current_output()
      self._set_result(idx, data)
    return

  def _next(self, event)  -> int:
    self._step('next')

  def current(self) -> int:
    return self._step('current')

  def _prev(self, event) -> int:
    return self._step('prev')

  @staticmethod
  def _get_image_from_output(output) ->np.dtype:
    image = None
    if output is not None:
      image = output['image']
    return image

  def _top(self, event) -> None:
    self._set_top_state()
    return
  
  def _set_top_state(self) -> None:
    self._view.image.set_result_image(None)
    if self._ready():
      self._view.flow.set_selection_tree()
      self._runner.reset()
    return


  @staticmethod
  def _convert_to_dict(params_def: List[Dict]) -> Dict:
    def compl():
      return param_def.get('p_types')      

    type_switcher = {
      'int': int,
      'float': float,
      'str': str,
      'bool': bool,
      'Range': compl,
      'List': compl,
      'Dict': compl
    }

    params = {}
    for param_def in params_def:
      name = param_def.get('name')
      value = param_def.get('default')
      vtype = param_def.get('type')
      converter = type_switcher.get(vtype)
      value = converter()   
      params[name] = value
    return params

  @staticmethod
  def _merge_params(params_new: Dict, params_def: List[Dict], params: Dict) -> Dict:
    # Mergre the new param set with current one:
    # for param in new param set:
    #  if a param is in current params set:
    #   if the current param value == new param value:
    #     continue
    #   else:
    #     upate current param value with new one
    #  else:
    #   if the new param value == default param value:
    #     continue
    #   else:
    #     add the pair {param: value} into current param set
    for param_new in params_new:
      name_new = param_new.get('name')
      value_new = param_new.get('value')
      if name_new in params:
        value = params.get(name_new)
        if value_new == value:
          continue
        else:
          params[name_new] = value_new
      else:
        value_def = params_def.get(name_new)
        if value_new == value_def:
          continue
        else:
          params[name_new] = value_new
    return params

# Operation parameters sub panel's commands
  def _update_current_flow_params(self) -> None:
    # get new params values from params view 
    params_new = self._view.flow.oper_params_view.get_operation_params_item()
    idx, item = self._view.flow.get_current_selection_tree()
    # get params defenitions and current flow params from the flow item 
    flow_item = self._model.flow.get_item(idx)
    params_def = flow_item.params_def
    params_dict = self._convert_to_dict(params_def)
    params = flow_item.params

    params = self._merge_params(params_new, params_dict, params)
    self._view.flow.oper_params_view.set_operation_params_from_dict(idx, item.get('text'), params, copy.deepcopy(params_def))
    return

  def _apply(self, event) -> None:
    self._update_current_flow_params()
    self.current()
    return

  def _reset(self, event) -> None:
    idx, item = self._view.flow.get_current_selection_tree()
    name = item.get('text')
    operation = self._model.module.get_operation_by_name(name)
    self._view.flow.oper_params_view.set_operation_params(idx, name, operation.params)
    fitem = self._model.flow.get_item(idx)
    fitem.params = {}
    self.current()
    return

  def _selected_path(self, event) -> None:
    item = self._view.image.names_combo_box.get()
    self._update_images_file_names_list(item)   
    return

  def _update_images_file_names_list(self, path) -> None:
    file_names_list = self._model.image.get_images_file_names_list(path)
    self._view.image.set_file_names_list(file_names_list)
    return

  def _image_file_selected(self, idx) -> None:
    if not idx:
      return
    self.file_idx = idx[0] 
    return

  def _load(self, event) -> None:
    return

  def _clear(self, event) -> None:
    return

  # def _get_cv2image(self) -> np.dtype:
  #   cv2image = None
  #   if self.file_idx is not None:
  #     idx = self.file_idx
  #     image_full_file_name = self._model.image.get_selected_file_full_name(idx)
  #     cv2image = self._model.image.get_image(image_full_file_name)
  #   return cv2image


  def _ready(self) -> bool:
    # if self.image_loaded and self._runner.initialized and self._model.flow.loaded:
    if self._runner.initialized and self._model.flow.loaded:
      self._view.flow.activate_buttons(True)
      return True
    else:
      self._view.flow.activate_buttons()
      return False

  def _rebuild_runner(self) -> None:
    if self._model.flow:
      self._runner.build(self._model.flow)
      # self._runner.reset()
    self._set_top_state()
    return
