import numpy as np

from ..configuration import Configuration
from flow_runner import Runner
from flow_converter import FlowConverter 
from .mngrmodel import MngrModel  
from .mngrconverter import MngrConverter  
from .mngrview import MngrView  

class MngrController():
  def __init__(self, parent):
    self.cfg = Configuration()
    self.runner = Runner()
    self.model = MngrModel(self.cfg)
    self.converter = MngrConverter()
    self.view = MngrView(parent)

# Bind to modules panel
    self.view.module_view.tree_view.bind('<<TreeviewOpen>>', self.open_all)
# Bind to flows panel
    self.flows_view_idx = 0  
    self.view.flow_view.names_combo_box.bind('<<ComboboxSelected>>', self.selected)
    self.view.flow_view.btn_add.bind("<Button>", self.add_step_to_flow_model)
    self.view.flow_view.btn_remove.bind("<Button>", self.remove_step_from_flow_model)
    self.view.flow_view.btn_reset.bind("<Button>", self.reset_flow_model)
    self.view.flow_view.btn_save.bind("<Button>", self.store_flow_model)
    self.view.flow_view.btn_run.bind("<Button>", self.run)
    self.view.flow_view.btn_next.bind("<Button>", self.next)
    self.view.flow_view.btn_prev.bind("<Button>", self.prev)
    self.view.flow_view.btn_top.bind("<Button>", self.top)
    self.view.flow_view.oper_params_view.btn_apply.bind("<Button>", self.apply)
    self.view.flow_view.oper_params_view.btn_reset.bind("<Button>", self.reset)
    self.view.flow_view.flow_tree_view.bind('<<TreeviewSelect>>', self.step_selected_tree)

# Bind to images panel
    # self.view.images_view.auto_input_check_button.bind('<<CheckbuttonChecked>>', lambda e: self.auto_input_changed(True))
    # self.view.images_view.auto_input_check_button.bind('<<CheckbuttonUnChecked>>', lambda e: self.auto_input_changed())
    self.view.image_view.btn_load.bind("<Button>", self.load)
    self.view.image_view.btn_clear.bind("<Button>", self.clear)
    self.view.image_view.names_combo_box.bind('<<ComboboxSelected>>', self.selected_path)  
    self.view.image_view.file_names_list_box.bind('<<ListboxSelect>>', 
      lambda e: self.image_file_selected(self.view.image_view.file_names_list_box.curselection()))

    self.init_mage = np.ones((10, 10, 3), dtype="uint8")*255 
    self.cv2image = self.init_mage
    self.view.image_view.set_result_image(self.cv2image)
    self.file_idx = None
    self.flow_meta = None
    self.start()
    
# Initialization
  def start(self):
    self.update_modules_view()
    self.update_flows_view()
    self.update_images_view()
    return

  def update_modules_view(self):
    modules_defs = self.converter.modulelist_to_module_defs(self.model.modulemodellists)
    self.view.module_defs = modules_defs
    return

  def update_flows_view(self):
    flow_names = self.converter.flowlist_to_flow_names(self.model.flowmodellist)
    self.view.flow_names = flow_names
    return


  def update_flow_model(self, model_name):
    self.view.flow_view.activate_buttons()
    flow_model = self.model.flowmodel(
        *self.converter.flow_name_to_path_name(model_name))
    self.flow_model = flow_model
    flow_names = self.converter.flow_model_to_module_names(flow_model)
    self.view.flow_view.set_flow_names(flow_names)
    self.rerun_fsm()
    return

  def rerun_fsm(self):
    if self.flow_model:
      fc = FlowConverter(self.flow_model)
      fsm_def = fc.convert()
      self.runner.create_frfsm(self.cfg.cfg_fsm, fsm_def)
      self.runner.start()
    self.set_top_state()
    return

  def update_images_view(self):
    self.view.image_view.set_input_paths(self.cfg.input_paths)
    return

  def update_images_file_names_list(self, path):
    file_names_list = self.model.images_model.get_images_file_names_list(path)
    self.view.image_view.set_file_names_list(file_names_list)
    return

# Actions
# Modules panel' events and commands
  def open_all(self, event):
    self.view.modules_view.open_all()
    return

# Flows panel's events and commands
  def selected(self, event):
    self.set_selected_flow_model()
    return

  def set_selected_flow_model(self):
    flow_name = self.view.flow_view.names_combo_box.get()
    self.update_flow_model(flow_name)
    self.view.flow_view.clear_operation_params()
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
    orig_image_size = self.model.images_model.get_original_image_size()
    oper_params_defenition = self.model.module_model.read_operation_params_defenition(module_name, oper_name)
    oper_params = self.converter.modules_converter.convert_params_defenition_to_params(step, oper_params_defenition, orig_image_size)
    return step_def, oper_params

  def set_operation_params(self, model, idx):
    if len(model) > 0:
      print('model.name', model.name)
      # step = meta[idx]
      # step_def, oper_params = self.get_operation_params(step)
      # self.view.flows_view.set_operation_params(idx, step_def, oper_params)
    return

  def step_selected_tree(self, event):
    idx = self.view.flow_view.get_current_selection_tree()
    # self.set_operation_params(self.flow_model, idx)
    return

  def add_step_to_flow_model(self, event):
    # Get destination item position after that will be added new one
    cur_idx = self.view.flow_view.get_current_selection_tree()
    # Get source item position from modules view
    operation_name = self.view.module_view.get_selected_operation_meta()   
    # Perform if operation only selected
    # if operation_name is not None:     
    #   step_def, oper_params = self.get_operation_params(operation_name)
    #   new_flow_model = self.model.flows_model.add_opearation_to_current_flow(step_def, oper_params, cur_idx)
    #   self.flow_model = new_flow_model
    #   new_flow_model = self.convert_flow_model(new_flow_model)
    #   self.view.flows_view.set_flow_model(new_flow_model, cur_idx+1)
    self.rerun_fsm()
    return

  def remove_step_from_flow_model(self, event):
    cur_idx = self.view.flow_view.get_current_selection_tree()
    new_flow_model = self.model.flow_model.remove_operation_from_current_flow(cur_idx)
    self.flow_meta = new_flow_model
    new_flow_model = self.convert_flow_model(new_flow_model)
    self.view.flow_view.set_flow_model(new_flow_model, cur_idx)
    self.rerun_fsm()
    return

  def reset_flow_model(self, event):
    self.set_selected_flow_model()
    self.rerun_fsm()
    return

  def store_flow_model(self, event):
    flow_name = self.view.flow_view.names_combo_box.get()
    path, name = self.converter.flow_converter.convert_ws_item(flow_name)
    self.model.flow_model.store_flow_model(path, name, self.flow_meta)
    self.update_flow_model(flow_name)
    self.set_top_state()
    return

# Execution commands
  def set_result(self, idx, cv2image):
    if cv2image is not None:
      self.view.image_view.set_result_image(cv2image)
    self.view.flow_view.set_selection_tree(idx)
    return

  def run(self, event):
    idx = 0
    if self.ready():
      idx, cv2image = self.runner.run_all(self.flow_model.items)
      self.set_result(idx, cv2image)
    return idx

  def step(self, event_name):
    idx = self.view.flow_view.get_current_selection_tree()
    if self.ready():
      flow_item = self.flow_model.items[idx]
      idx, cv2image = self.runner.run_step(event_name, flow_item)
      self.set_result(idx, cv2image)
    return idx

  def next(self, event):
    return self.step('next')

  def current(self):
    return self.step('current')

  def prev(self, event):
    return self.step('prev')

  @staticmethod
  def get_image_from_output(output):
    image = None
    if output is not None:
      image = output['image']
    return image

  def top(self, event):
    if self.ready():
      self.runner.start()
      self.set_top_state()
    return
  
  def set_top_state(self):
    if self.image_loaded:
      self.view.image_view.set_result_image(self.cv2image)
    if self.ready():
      self.view.flow_view.set_selection_tree()
      self.runner.init_storage(self.cv2image) 
    return

# Operation parameters sub panel's commands
  def update_current_flow_params(self):
    operation_params_item = self.view.flow_view.oper_params_view.get_operation_params_item()
    self.model.flow_model.update_current_flow_params(operation_params_item)
    # self.view.flows_view.flow_tree_view.focus_set()
    if self.image_loaded():
      self.current()
    return

  def ready(self):
    if self.image_loaded and self.runner.initialized and self.flow_model.loaded:
      self.view.flow_view.activate_buttons(True)
      return True
    else:
      self.view.flow_view.activate_buttons()
      return False

  def apply(self, event):
    self.update_current_flow_params()
    return

  def reset(self, event):
    idx = self.view.flow_view.get_current_selection_tree()
    item = self.view.flow_view.names_combo_box.get()      
    orig_flow_model = self.model.flow_model.get_worksheet(*self.converter.flow_converter.convert_ws_item(item))
    self.set_operation_params(orig_flow_model, idx)
    self.update_current_flow_params()   
    return

# Images panel's commands
  @property
  def image_loaded(self) ->bool:
    return self.cv2image is not None

  def selected_path(self, event):
    item = self.view.image_view.names_combo_box.get()
    self.update_images_file_names_list(item)   
    return

  def image_file_selected(self, idx):
    if not idx:
      return
    self.file_idx = idx[0] 
    return

  def load(self, event):
    self.cv2image = self.get_cv2image()
    # self.rerun_fsm()
    self.set_top_state()
    return

  def clear(self, event):
    self.cv2image = self.init_mage
    self.view.images_view.set_result_image(self.cv2image)
    self.set_top_state()
    return

  def get_cv2image(self):
    cv2image = None
    if self.file_idx is not None:
      idx = self.file_idx
      image_full_file_name = self.model.images_model.get_selected_file_full_name(idx)
      cv2image = self.model.images_model.get_image(image_full_file_name)
    return cv2image

  # def auto_input_changed(self, new_state=False):
  #   self.use_auto_input = new_state
  #   self.cv2image = self.init_mage
  #   self.view.images_view.set_result_image(self.cv2image)
  #   self.view.images_view.activate_controls(not new_state)
  #   self.set_top_state()
  #   return