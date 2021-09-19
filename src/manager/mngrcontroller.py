import numpy as np

from ..configuration import Configuration
from flow_runner import Runner
from flow_converter import FlowConverter 
from .mngrmodel import MngrModel  
from .mngrconverter import MngrConverter  
from .mngrview import MngrView  

class MngrController():
  def __init__(self, parent):
    self.parent = parent
    self.cfg = Configuration()
    self.runner = Runner()
    self.model = MngrModel(self.cfg)
    self.converter = MngrConverter()
    self.view = MngrView(self.parent)

# Bind to modules panel
    self.view.modules_view.tree_view.bind('<<TreeviewOpen>>', self.open_all)
# Bind to flows panel
    self.flows_view_idx = 0  
    self.view.flows_view.names_combo_box.bind('<<ComboboxSelected>>', self.selected)
    self.view.flows_view.btn_add.bind("<Button>", self.add_step_to_flow_meta)
    self.view.flows_view.btn_remove.bind("<Button>", self.remove_step_from_flow_meta)
    self.view.flows_view.btn_reset.bind("<Button>", self.reset_flow_meta)
    self.view.flows_view.btn_save.bind("<Button>", self.store_flow_meta)

    self.view.flows_view.btn_run.bind("<Button>", self.run)
    self.view.flows_view.btn_next.bind("<Button>", self.next)
    self.view.flows_view.btn_prev.bind("<Button>", self.prev)
    self.view.flows_view.btn_top.bind("<Button>", self.top)

    self.view.flows_view.oper_params_view.btn_apply.bind("<Button>", self.apply)
    self.view.flows_view.oper_params_view.btn_reset.bind("<Button>", self.reset)
    self.view.flows_view.flow_tree_view.bind('<<TreeviewSelect>>', self.step_selected_tree)

# Bind to images panel
    # self.view.images_view.auto_input_check_button.bind('<<CheckbuttonChecked>>', lambda e: self.auto_input_changed(True))
    # self.view.images_view.auto_input_check_button.bind('<<CheckbuttonUnChecked>>', lambda e: self.auto_input_changed())
    self.view.images_view.btn_load.bind("<Button>", self.load)
    self.view.images_view.btn_clear.bind("<Button>", self.clear)

    self.view.images_view.names_combo_box.bind('<<ComboboxSelected>>', self.selected_path)  
    self.view.images_view.file_names_list_box.bind('<<ListboxSelect>>', 
      lambda e: self.image_file_selected(self.view.images_view.file_names_list_box.curselection()))

    self.init_mage = np.ones((10, 10, 3), dtype="uint8")*255 
    self.cv2image = self.init_mage
    self.view.images_view.set_result_image(self.cv2image)
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
    # TODO: add wrappers to MngrModel & MngrConverter
    self.model.modules_model.load_modules_meta_from_all_paths()
    modules_meta_conv = self.converter.modules_converter.convert_meta(
      self.model.modules_model.get_modules_meta())
    self.view.modules_view.set_modules_meta(modules_meta_conv)
    return

  def update_flows_view(self):
    # TODO: add wrappers to MngrModel & MngrConverter
    self.model.flows_model.load_worksheets_from_all_paths()
    worksheets_names = self.converter.flows_converter.convert_worksheets_names(
      self.model.flows_model.get_worksheets_names_from_all_paths())
    self.view.flows_view.set_worksheets_names(worksheets_names)
    return

  def convert_flow_meta(self, meta):
    return self.converter.flows_converter.convert_flow_meta(meta)

  def update_flow_meta(self, item):
    self.view.flows_view.activate_buttons()
    flow_meta = self.model.flows_model.load_flow_meta(
        *self.converter.flows_converter.convert_ws_item(item))
    self.flow_meta = flow_meta
    flow_meta = self.convert_flow_meta(flow_meta)
    self.view.flows_view.set_flow_meta(flow_meta)
    self.rerun_fsm()
    return

  def rerun_fsm(self):
    if self.flow_meta:
      fc = FlowConverter(self.flow_meta)
      fsm_def = fc.convert()
      self.runner.init_fsm_engine(self.cfg.get_fsm_cfg(), fsm_def)
      self.runner.start()
    self.set_top_state()
    return

  def update_images_view(self):
    paths = self.model.images_model.get_input_paths()
    self.view.images_view.set_input_paths(paths)
    return

  def update_images_file_names_list(self, path):
    file_names_list = self.model.images_model.get_images_file_names_list(path)
    self.view.images_view.set_file_names_list(file_names_list)
    return

# Actions
# Modules panel' events and commands
  def open_all(self, event):
    self.view.modules_view.open_all()
    return

# Flows panel's events and commands
  def selected(self, event):
    self.set_selected_flow_meta()
    return

  def set_selected_flow_meta(self):
    item = self.view.flows_view.names_combo_box.get()
    self.update_flow_meta(item)
    self.view.flows_view.clear_operation_params()
    return

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
    oper_params_defenition = self.model.modules_model.read_operation_params_defenition(module_name, oper_name)
    oper_params = self.converter.modules_converter.convert_params_defenition_to_params(step, oper_params_defenition, orig_image_size)
    return step_def, oper_params

  def set_operation_params(self, meta, idx):
    if len(meta) > 0:
      step = meta[idx]
      step_def, oper_params = self.get_operation_params(step)
      self.view.flows_view.set_operation_params(idx, step_def, oper_params)
    return

  def step_selected_tree(self, event):
    idx = self.view.flows_view.get_current_selection_tree()
    self.set_operation_params(self.flow_meta, idx)
    return

  def add_step_to_flow_meta(self, event):
    # Get destination item position after that will be added new one
    cur_idx = self.view.flows_view.get_current_selection_tree()
    # Get source item position from modules view
    operation_meta = self.view.modules_view.get_selected_operation_meta()   
    # Perform if operation only selected
    if operation_meta is not None:     
      step_def, oper_params = self.get_operation_params(operation_meta)
      new_flow_meta = self.model.flows_model.add_opearation_to_current_flow(step_def, oper_params, cur_idx)
      self.flow_meta = new_flow_meta
      new_flow_meta = self.convert_flow_meta(new_flow_meta)
      self.view.flows_view.set_flow_meta(new_flow_meta, cur_idx+1)
    self.rerun_fsm()
    return

  def remove_step_from_flow_meta(self, event):
    cur_idx = self.view.flows_view.get_current_selection_tree()
    new_flow_meta = self.model.flows_model.remove_operation_from_current_flow(cur_idx)
    self.flow_meta = new_flow_meta
    new_flow_meta = self.convert_flow_meta(new_flow_meta)
    self.view.flows_view.set_flow_meta(new_flow_meta, cur_idx)
    self.rerun_fsm()
    return

  def reset_flow_meta(self, event):
    self.set_selected_flow_meta()
    self.rerun_fsm()
    return

  def store_flow_meta(self, event):
    item = self.view.flows_view.names_combo_box.get()
    path, name = self.converter.flows_converter.convert_ws_item(item)
    self.model.flows_model.store_flow_meta(path, name, self.flow_meta)
    self.update_flow_meta(item)
    self.set_top_state()
    return

# Execution commands
  def set_result(self, idx, cv2image):
    if cv2image is not None:
      self.view.images_view.set_result_image(cv2image)
    self.view.flows_view.set_selection_tree(idx)
    return

  def run(self, event):
    idx = 0
    if self.ready():
      idx, cv2image = self.runner.run_all(self.flow_meta)
      self.set_result(idx, cv2image)
    return idx

  def step(self, event_name):
    idx = self.view.flows_view.get_current_selection_tree()
    if self.ready():
      step_meta = self.flow_meta[idx]
      idx, cv2image = self.runner.run_step(event_name, step_meta)
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
    if self.image_loaded():
      self.view.images_view.set_result_image(self.cv2image)
    if self.ready():
      self.view.flows_view.set_selection_tree()
      self.runner.init_io(self.cv2image) 
    return

# Operation parameters sub panel's commands
  def update_current_flow_params(self):
    operation_params_item = self.view.flows_view.oper_params_view.get_operation_params_item()
    self.model.flows_model.update_current_flow_params(operation_params_item)
    self.view.flows_view.flow_tree_view.focus_set()
    if self.image_loaded():
      self.current()
    return

  def image_loaded(self):
    return self.cv2image is not None

  def ready(self):
    if self.image_loaded() and self.runner.initialized() and len(self.flow_meta) > 0:
      self.view.flows_view.activate_buttons(True)
      return True
    else:
      self.view.flows_view.activate_buttons()
      return False

  def apply(self, event):
    self.update_current_flow_params()
    return

  def reset(self, event):
    idx = self.view.flows_view.get_current_selection_tree()
    item = self.view.flows_view.names_combo_box.get()      
    orig_flow_meta = self.model.flows_model.get_worksheet(*self.converter.flows_converter.convert_ws_item(item))
    self.set_operation_params(orig_flow_meta, idx)
    self.update_current_flow_params()   
    return

# Images panel's commands
  def selected_path(self, event):
    item = self.view.images_view.names_combo_box.get()
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