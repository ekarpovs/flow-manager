import numpy as np
import copy

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
    self._view.module.tree_view.bind('<<TreeviewOpen>>', self.open_all)
# Bind to flows panel
    self.flows_view_idx = 0  
    self._view.flow.names_combo_box.bind('<<ComboboxSelected>>', self.selected)
    self._view.flow.btn_add.bind("<Button>", self.add_operation_to_flow_model)
    self._view.flow.btn_remove.bind("<Button>", self.remove_operation_from_flow_model)
    self._view.flow.btn_reset.bind("<Button>", self.reset_flow_model)
    self._view.flow.btn_save.bind("<Button>", self.store_flow_model)
    self._view.flow.btn_run.bind("<Button>", self.run)
    self._view.flow.btn_next.bind("<Button>", self.next)
    self._view.flow.btn_prev.bind("<Button>", self.prev)
    self._view.flow.btn_top.bind("<Button>", self.top)
    self._view.flow.oper_params_view.btn_apply.bind("<Button>", self.apply)
    self._view.flow.oper_params_view.btn_reset.bind("<Button>", self.reset)
    self._view.flow.flow_tree_view.bind('<<TreeviewSelect>>', self.tree_selection_changed)

# Bind to images panel
    # self._view.images_view.auto_input_check_button.bind('<<CheckbuttonChecked>>', lambda e: self.auto_input_changed(True))
    # self._view.images_view.auto_input_check_button.bind('<<CheckbuttonUnChecked>>', lambda e: self.auto_input_changed())
    self._view.image.btn_load.bind("<Button>", self.load)
    self._view.image.btn_clear.bind("<Button>", self.clear)
    self._view.image.names_combo_box.bind('<<ComboboxSelected>>', self.selected_path)  
    self._view.image.file_names_list_box.bind('<<ListboxSelect>>', 
      lambda e: self.image_file_selected(self._view.image.file_names_list_box.curselection()))

    self.init_mage = np.ones((10, 10, 3), dtype="uint8")*255 
    self.cv2image = self.init_mage
    self._view.image.set_result_image(self.cv2image)
    self.file_idx = None
    self.flow_model = None
    self.start()
    
# Initialization
  def start(self) -> None:
    self.update_module_view()
    self.update_worksheet_list()
    self.update_image_view()
    return

  def update_module_view(self) -> None:
    module_defs = self._converter.modulelist_to_module_defs(self._model.module)
    self._view.module_defs = module_defs
    return

  def update_worksheet_list(self) -> None:
    names = self._model._worksheet.workseetnames
    names.insert(0, 'new <>')
    self._view.ws_names = names
    return


  def update_flow_model(self, ws_name) -> None:
    self._view.flow.activate_buttons()
    (ws_path, ws_name) = self._converter.split_ws_name(ws_name)
    # read worksheet
    ws = self._model._worksheet.read(ws_path, ws_name)
    # Create active flow model
    self._model.create_active_flow_model(ws_path, ws_name, ws)
    self._model.flow
    names = self._model.flow.names()
    self._view.flow.set_flow_names(names)
    # Merge active flow model's operations with operations definitions from module models
    
    self.rerun_fsm()
    return

  def rerun_fsm(self) -> None:
    if self._model.flow:
      fc = FlowConverter(self._model.flow.active)
      fsm_def = fc.convert()
      self._runner.create_frfsm(self.cfg.cfg_fsm, fsm_def)
      self._runner.start()
    self.set_top_state()
    return

  def update_image_view(self) -> None:
    self._view.image.set_input_paths(self.cfg.input_paths)
    return

  def update_images_file_names_list(self, path) -> None:
    file_names_list = self._model.image.get_images_file_names_list(path)
    self._view.image.set_file_names_list(file_names_list)
    return

# Actions
# Modules panel' events and commands
  def open_all(self, event) -> None:
    self._view.module.open_all()
    return

# Flows panel's events and commands
  def selected(self, event) -> None:
    self.set_selected_flow_model()
    return

  def set_selected_flow_model(self) -> None:
    flow_name = self._view.flow.names_combo_box.get()
    self.update_flow_model(flow_name)
    self._view.flow.clear_operation_params()
    return

# !!! Parameters 
  def get_operation_params(self, step):
    if type(step) is dict:
      if 'exec' in step:
        step_def = step['exec'] 
      elif 'stm' in step:
        step_def = step['stm']
    else:
      step_def = step   

    module_name, oper_name = step_def.split('.')
    orig_image_size = self._model.image.get_original_image_size()
    oper_params_defenition = self._model.module.read_operation_params_defenition(module_name, oper_name)
    oper_params = self._converter.module.convert_params_defenition_to_params(step, oper_params_defenition, orig_image_size)
    return step_def, oper_params

  def set_operation_params(self, model, idx):
    if len(model) > 0:
      print('model.name', model.name)
      # step = meta[idx]
      # step_def, oper_params = self.get_operation_params(step)
      # self._view.flows_view.set_operation_params(idx, step_def, oper_params)
    return

  def tree_selection_changed(self, event) -> None:
    idx = self._view.flow.get_current_selection_tree()
    # self.set_operation_params(self.flow_model, idx)
    return

  def add_operation_to_flow_model(self, event):
    # Get destination item position after that will be added new one
    cur_idx = self._view.flow.get_current_selection_tree()
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

  def remove_operation_from_flow_model(self, event):
    cur_idx = self._view.flow.get_current_selection_tree()
    new_flow_model = self._model.flow.remove_operation_from_current_flow(cur_idx)
    self.flow_model = new_flow_model
    new_flow_model = self.convert_flow_model(new_flow_model)
    self._view.flow.set_flow_model(new_flow_model, cur_idx)
    self.rerun_fsm()
    return

  def reset_flow_model(self, event):
    self.set_selected_flow_model()
    self.rerun_fsm()
    return

  def store_flow_model(self, event):
    flow_name = self._view.flow.names_combo_box.get()
    path, name = self._converter.flow.convert_ws_item(flow_name)
    self._model.flow.store_flow_model(path, name, self.flow_model)
    self.update_flow_model(flow_name)
    self.set_top_state()
    return

# Execution commands
  def set_result(self, idx, cv2image) -> None:
    if cv2image is not None:
      self._view.image.set_result_image(cv2image)
    self._view.flow.set_selection_tree(idx)
    return

  def run(self, event) -> int:
    idx = 0
    if self.ready():
      idx, cv2image = self._runner.run_all(self._model.flow.active.items)
      self.set_result(idx, cv2image)
    return idx

  def step(self, event_name) -> int:
    idx = self._view.flow.get_current_selection_tree()
    if self.ready():
      flow_item = self._model.flow.active.items[idx]
      idx, cv2image = self._runner.run_step(event_name, flow_item)
      self.set_result(idx, cv2image)
    return idx

  def next(self, event)  -> int:
    return self.step('next')

  def current(self) -> int:
    return self.step('current')

  def prev(self, event) -> int:
    return self.step('prev')

  @staticmethod
  def get_image_from_output(output) ->np.dtype:
    image = None
    if output is not None:
      image = output['image']
    return image

  def top(self, event) -> None:
    if self.ready():
      self._runner.start()
      self.set_top_state()
    return
  
  def set_top_state(self) -> None:
    if self.image_loaded:
      self._view.image.set_result_image(self.cv2image)
    if self.ready():
      self._view.flow.set_selection_tree()
      self._runner.init_storage(self.cv2image) 
    return

# Operation parameters sub panel's commands
  def update_current_flow_params(self):
    operation_params_item = self._view.flow.oper_params_view.get_operation_params_item()
    self._model.flow.update_current_flow_params(operation_params_item)
    # self._view.flows_view.flow_tree_view.focus_set()
    if self.image_loaded():
      self.current()
    return

  def ready(self) -> bool:
    if self.image_loaded and self._runner.initialized and self._model.flow.active.loaded:
      self._view.flow.activate_buttons(True)
      return True
    else:
      self._view.flow.activate_buttons()
      return False

  def apply(self, event):
    self.update_current_flow_params()
    return

  def reset(self, event):
    idx = self._view.flow.get_current_selection_tree()
    item = self._view.flow.names_combo_box.get()        
    # orig_flow_model = self._model.flow.get_worksheet(*self._converter.flow.convert_ws_item(item))
    # self.set_operation_params(orig_flow_model, idx)
    # self.update_current_flow_params()   
    return

# Images panel's commands
  @property
  def image_loaded(self) ->bool:
    return self.cv2image is not None

  def selected_path(self, event) -> None:
    item = self._view.image.names_combo_box.get()
    self.update_images_file_names_list(item)   
    return

  def image_file_selected(self, idx) -> None:
    if not idx:
      return
    self.file_idx = idx[0] 
    return

  def load(self, event) -> None:
    self.cv2image = self.get_cv2image()
    self.set_top_state()
    return

  def clear(self, event) -> None:
    self.cv2image = self.init_mage
    self._view.image.set_result_image(self.cv2image)
    self.set_top_state()
    return

  def get_cv2image(self) -> np.dtype:
    cv2image = None
    if self.file_idx is not None:
      idx = self.file_idx
      image_full_file_name = self._model.image.get_selected_file_full_name(idx)
      cv2image = self._model.image.get_image(image_full_file_name)
    return cv2image
