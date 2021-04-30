from src.manager.models import model
from tkinter import image_names
from .runner import Runner  
from .mngrmodel import MngrModel  
from .mngrconverter import MngrConverter  
from .mngrview import MngrView  
from ..configuration import Configuration

class MngrController():
  def __init__(self, parent):
    self.parent = parent

    self.cfg = Configuration()

    self.runner = Runner(self.cfg)
    self.model = MngrModel(self.cfg)
    self.converter = MngrConverter()
    self.view = MngrView(self.parent)

    # Bind to modules panel

    # Bind to flows panel
    self.view.flows_view.names_combo_box.bind('<<ComboboxSelected>>', self.selected)
    self.view.flows_view.flow_list_box.bind('<<ListboxSelect>>', 
      lambda e: self.step_selected(self.view.flows_view.flow_list_box.curselection()))
    self.view.flows_view.flow_list_box.bind("<Double-1>", 
      lambda e: self.step_update(self.view.flows_view.flow_list_box.curselection()))

    self.view.flows_view.btn_add.bind("<Button>", self.add)
    self.view.flows_view.btn_remove.bind("<Button>", self.remove)

    self.view.flows_view.btn_run.bind("<Button>", self.run)
    self.view.flows_view.btn_step.bind("<Button>", self.step)
    self.view.flows_view.btn_back.bind("<Button>", self.back)
    self.view.flows_view.btn_top.bind("<Button>", self.top)

    self.view.flows_view.oper_params_view.btn_apply.bind("<Button>", self.apply)
    self.view.flows_view.oper_params_view.btn_save.bind("<Button>", self.save)
    self.view.flows_view.oper_params_view.btn_reset.bind("<Button>", self.reset)

    # Bind to images panel
    self.view.images_view.btn_load.bind("<Button>", self.load)
    self.view.images_view.names_combo_box.bind('<<ComboboxSelected>>', self.selected_path)
    self.view.images_view.file_names_list_box.bind('<<ListboxSelect>>', 
      lambda e: self.image_file_selected(self.view.images_view.file_names_list_box.curselection()))

    self.file_idx = None

    self.start()

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

  def update_flow_meta(self, item):
    flow_meta = self.model.flows_model.get_flow_meta(
        *self.converter.flows_converter.convert_ws_item(item))
    self.flow_meta = flow_meta
    flow_meta = self.converter.flows_converter.convert_flow_meta(flow_meta)

    self.view.flows_view.set_flow_meta(flow_meta)

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

  # Modules panel

  # Flows panel
  def selected(self, event):
    item = self.view.flows_view.names_combo_box.get()
    self.update_flow_meta(item)
    self.view.flows_view.clear_operation_params()
    self.set_top_state()

    return

  def step_selected(self, idx):
    if not idx:
      return
       
    step = self.flow_meta['steps'][idx[0]]
    module_name, oper_name = step['exec'].split('.')
    doc = self.model.modules_model.read_operation_doc(module_name, oper_name)
    oper_params_defenition = self.converter.flows_converter.filter_oper_doc(doc)
    # !!!!!!! MERGE WITH REAL PARAMETERS FROM FLOW META !!!!!!!!
    oper_params = []
    for param_def in oper_params_defenition:
      t, d, pvs, df, l = self.view.flows_view.oper_params_view.parse_single_param(param_def)
      p_name = l.split(':')[0].strip()
      if p_name in step:
        p_value = step[p_name]
        print("p_value", p_value)
      else:
        p_value = df

      oper_params.append({"type": t, "domain": d, "p_values": pvs, "name": p_name, "value": p_value, "label": l})
      
    self.view.flows_view.set_operation_params(idx[0], step['exec'], oper_params)

    return    

  def step_update(self, idx):
    print("update idx", idx[0], self.flow_meta['steps'][idx[0]])

    return    

  def add(self, event):
    # Get destination item position after that will be added new one
    cur_idx = self.view.flows_view.flow_list_box.curselection()[0]
    # Get source item position from modules view
    operation_meta = self.view.modules_view.get_selected_operation_meta()
    # Perform if operation only selected
    if operation_meta is not None:
      new_flow_meta = self.model.flows_model.add_opearation_to_current_flow(operation_meta, cur_idx+1)
      new_flow_meta = self.converter.flows_converter.convert_flow_meta(new_flow_meta)
      self.view.flows_view.set_flow_meta(new_flow_meta)

    return

  def remove(self, event):
    cur_idx = self.view.flows_view.flow_list_box.curselection()[0]
    self.model.flows_model.remove_operation_from_current_flow(cur_idx)
    self.view.flows_view.flow_list_box.delete(cur_idx, cur_idx)

    return

  def run(self, event):
    # Move to runner
    counter, cv2image = self.runner.run(self.flow_meta) 
    self.view.images_view.set_result_image(cv2image)
    self.view.flows_view.set_next_selection(counter)

  
  def step(self, event):
    counter, cv2image = self.runner.run(self.flow_meta, True)
    if cv2image is not None:
      self.view.images_view.set_result_image(cv2image)
      self.view.flows_view.set_next_selection(counter)

  def back(self, event):
    counter, cv2image = self.runner.back()
    if cv2image is not None:
      self.view.images_view.set_result_image(cv2image)
      self.view.flows_view.set_next_selection(counter, back=True)
    else:
      print("clean the output image")
      self.view.images_view.reset_result_image()


  def top(self, event):
    self.set_top_state()
    return
  
  def set_top_state(self):
    self.runner.top()
    print("clean the output image")
    self.view.images_view.reset_result_image()
    self.view.flows_view.set_first_selection()

    return

  # Operation parameters sub panel
  def apply(self, event):
    operation_params_item = self.view.flows_view.oper_params_view.get_operation_params_item()
    self.model.flows_model.update_current_flow_params(operation_params_item)
    
    return

  def save(self, event):
    operation_params_item = self.view.flows_view.oper_params_view.get_operation_params_item()
    self.model.flows_model.update_current_flow_params(operation_params_item)
    
    return


  def reset(self, event):
    print("reset by the operation defaults params")

    return


# Images panel
  def selected_path(self, event):
    item = self.view.images_view.names_combo_box.get()
    self.update_images_file_names_list(item)
    self.set_top_state()
    
    return

  def image_file_selected(self, idx):
    if not idx:
      return
    self.file_idx = idx[0]
    
    return

  def load(self, event):
    self.set_top_state()

    idx = self.file_idx
    image_full_file_name = self.model.images_model.get_selected_file_full_name(idx)

    cv2image = self.model.images_model.get_image(image_full_file_name)
    self.runner.set_input_image(cv2image) 
    self.view.images_view.set_original_image(cv2image)
