from flow_model.flowmodel import FlowModel
import numpy as np
import copy

from src.manager.models.module.modulemodel import ModuleModel
from src.manager.models.module.modulemodellist import ModuleModelList

from ..configuration import Configuration
from flow_runner import Runner
from flow_converter import FlowConverter 
from .mngrmodel import MngrModel  
from .mngrconverter import MngrConverter  
from .mngrview import MngrView  

class MngrController():
  def __init__(self, parent):
    self.cfg = Configuration()
    self._runner = Runner()
    self._model = MngrModel(self.cfg)
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
    self._view.flow.btn_save.bind("<Button>", self._store_flow_model)
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

    self.init_mage = np.ones((10, 10, 3), dtype="uint8")*255 
    self.cv2image = self.init_mage
    self._view.image.set_result_image(self.cv2image)
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

  # When worksheet item is selected
  def _init_flow_model(self, ws_name) -> None:
    self._view.flow.activate_buttons()
    (ws_path, ws_name) = self._converter.split_ws_name(ws_name)
    # read worksheet
    ws = self._model._worksheet.read(ws_path, ws_name)
    # Create current flow model
    self._model.create_flow_model(ws)
    names = self._model.flow.get_names()
    self._view.flow.set_flow_item_names(names)   

    self._rerun_fsm()
    return


  def _tree_selection_changed(self, event) -> None:
    idx, item = self._view.flow.get_current_selection_tree()
    name = item.get('text')
    self._view.flow.clear_operation_params()
    # Update the flow items models with default operations parameters
    operation = self._model.module.get_operation_by_name(name)
    item = self._model.flow.get_item(idx)
    item.params_def = operation.params
    self._view.flow.set_operation_params(idx, name, operation.params)



    # self._set_operation_params(idx, name)
    return



# !!! Parameters 
  def _set_operation_params(self, idx, operation_name):
    if self._model.flow is not None:
      item = self._model.flow.get_item(idx)
      # Merge default and current params
      params_def = item.params_def
      new_params = params_def
      params = item.params
      if params is not None and len(params) > 0:
        # params = params.get('params')
        for param_def in params_def:
          pname_def = param_def.get('name')
          for param in params:
          # param = params.get('params').get(pname_def)
            if param.get('name') == pname_def:
              new_param = new_params.get(pname_def)
              new_param = param
      if new_params is not None:
        self._view.flow.set_operation_params(idx, operation_name, new_params)
    return



  # def get_operation_params(self, step):
  #   if type(step) is dict:
  #     if 'exec' in step:
  #       step_def = step['exec'] 
  #     elif 'stm' in step:
  #       step_def = step['stm']
  #   else:
  #     step_def = step   

  #   module_name, oper_name = step_def.split('.')
  #   orig_image_size = self._model.image.get_original_image_size()
  #   oper_params_defenition = self._model.module.read_operation_params_defenition(module_name, oper_name)
  #   oper_params = self._converter.module.convert_params_defenition_to_params(step, oper_params_defenition, orig_image_size)
  #   return step_def, oper_params


  def _add_operation_to_flow_model(self, event):
    # Get destination item position after that will be added new one
    cur_idx,_ = self._view.flow.get_current_selection_tree()
    # Get source item position from modules view
    operation_name = self._view.module.get_selected_operation_meta()   
    # Perform if operation only selected
    # if operation_name is not None:     
    #   step_def, oper_params = self.get_operation_params(operation_name)
    #   new_flow_model = self._model.flows_model.add_opearation_to_current_flow(step_def, oper_params, cur_idx)
    #   self.flow_model = new_flow_model
    #   new_flow_model = self.convert_flow_model(new_flow_model)
    #   self._view.flows_view.set_flow_model(new_flow_model, cur_idx+1)
    self.rerun_fsm()
    return

  def _remove_operation_from_flow_model(self, event):
    cur_idx, _ = self._view.flow.get_current_selection_tree()
    new_flow_model = self._model.flow.remove_operation_from_current_flow(cur_idx)
    self._model.flow = new_flow_model
    new_flow_model = self.convert_flow_model(new_flow_model)
    self._view.flow.set_flow_model(new_flow_model, cur_idx)
    self.rerun_fsm()
    return

  def _reset_flow_model(self, event):
    self.set_selected_flow_model()
    self.rerun_fsm()
    return

  def _store_flow_model(self, event):
    flow_name = self._view.flow.names_combo_box.get()
    path, name = self._converter.flow.convert_ws_item(flow_name)
    self._model.flow.store_flow_model(path, name, self._model.flow)
    # self.update_flow_model(flow_name)
    self._set_top_state()
    return

# Execution commands
  def _set_result(self, idx, cv2image) -> None:
    if cv2image is not None:
      self._view.image.set_result_image(cv2image)
    self._view.flow.set_selection_tree(idx)
    return

  def _run(self, event) -> int:
    idx = 0
    if self._ready():
      idx, cv2image = self._runner.run_all(self._model.flow.items)
      self.set_result(idx, cv2image)
    return idx

  def _step(self, event_name) -> int:
    idx, item = self._view.flow.get_current_selection_tree()
    if self._ready():
      flow_item = self._model.flow.get_item(idx)
      idx, cv2image = self._runner.run_step(event_name, flow_item)
      self._set_result(idx, cv2image)
    return idx

  def _next(self, event)  -> int:
    return self._step('next')

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
    if self._ready():
      self._runner.start()
      self._set_top_state()
    return
  
  def _set_top_state(self) -> None:
    if self.image_loaded:
      self._view.image.set_result_image(self.cv2image)
    if self._ready():
      self._view.flow.set_selection_tree()
      self._runner.init_storage(self.cv2image) 
    return

# Operation parameters sub panel's commands
  def _update_current_flow_params(self):
    operation_params_item = self._view.flow.oper_params_view.get_operation_params_item()
    idx, item = self._view.flow.get_current_selection_tree()
    name = item.get('text')
    flow_item = self._model.flow.get_item(name)
    flow_item.params = operation_params_item
    if self.image_loaded:
      self.current()
    return

  def _ready(self) -> bool:
    if self.image_loaded and self._runner.initialized and self._model.flow.loaded:
      self._view.flow.activate_buttons(True)
      return True
    else:
      self._view.flow.activate_buttons()
      return False

  def _apply(self, event):
    self.update_current_flow_params()
    return

  def _reset(self, event):
    idx, item = self._view.flow.get_current_selection_tree()
    item = self._view.flow.names_combo_box.get()        
    # orig_flow_model = self._model.flow.get_worksheet(*self._converter.flow.convert_ws_item(item))
    # self.set_operation_params(orig_flow_model, idx)
    # self.update_current_flow_params()   
    return

# Images panel's commands
  @property
  def image_loaded(self) ->bool:
    return self.cv2image is not None

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
    self.cv2image = self._get_cv2image()
    self._set_top_state()
    return

  def _clear(self, event) -> None:
    self.cv2image = self.init_mage
    self._view.image.set_result_image(self.cv2image)
    self._set_top_state()
    return

  def _get_cv2image(self) -> np.dtype:
    cv2image = None
    if self.file_idx is not None:
      idx = self.file_idx
      image_full_file_name = self._model.image.get_selected_file_full_name(idx)
      cv2image = self._model.image.get_image(image_full_file_name)
    return cv2image

  def _rerun_fsm(self) -> None:
    if self._model.flow:
      fc = FlowConverter(self._model.flow)
      fsm_def = fc.convert()
      self._runner.create_frfsm(self.cfg.cfg_fsm, fsm_def)
      self._runner.start()
    self._set_top_state()
    return
