from tkinter import image_names
from .runner import Runner  
from .mngrmodel import MngrModel  
from .mngrconverter import MngrConverter  
from .mngrview import MngrView  
from ..configuration import Configuration

class MngrController():
  def __init__(self, parent):
    self.parent = parent

    print("MNGR-CONTROLLER")

    self.cfg = Configuration()

    self.runner = Runner(self.cfg)
    self.model = MngrModel(self.cfg)
    self.converter = MngrConverter()
    self.view = MngrView(self.parent)

    # Bind to flows panel
    self.view.flows_view.names_combo_box.bind('<<ComboboxSelected>>', self.selected)
    self.view.flows_view.flow_list_box.bind('<<ListboxSelect>>', 
      lambda e: self.step_selected(self.view.flows_view.flow_list_box.curselection()))
    self.view.flows_view.flow_list_box.bind("<Double-1>", 
      lambda e: self.step_update(self.view.flows_view.flow_list_box.curselection()))
    self.view.flows_view.btn_load.bind("<Button>", self.load)
    self.view.flows_view.btn_run.bind("<Button>", self.run)
    self.view.flows_view.btn_step.bind("<Button>", self.step)
    self.view.flows_view.btn_back.bind("<Button>", self.back)
    self.view.flows_view.btn_top.bind("<Button>", self.top)
   
    self.start()

  def start(self):
    self.update_modules_view()
    self.update_flows_view()

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


# Actions
  def selected(self, event):
    item = self.view.flows_view.names_combo_box.get()
    self.update_flow_meta(item)
    
    return

  def step_selected(self, idx):
    print("selected idx", idx[0], self.flow_meta['steps'][idx[0]])
    return    

  def step_update(self, idx):
    print("update idx", idx[0], self.flow_meta['steps'][idx[0]])

    return    


  def run(self, event):
    # Move to runner
    cv2image = self.runner.run_flow(self.flow_meta) 
    self.view.output_view.set_result_image(cv2image)

  
  def step(self, event):
    cv2image = self.runner.run_step(self.flow_meta)
    if cv2image is not None:
      self.view.output_view.set_result_image(cv2image)

  def back(self, event):
    cv2image = self.runner.step_back()
    if cv2image is not None:
      self.view.output_view.set_result_image(cv2image)
    else:
      print("clean the output image")
      self.view.output_view.reset_result_image()


  def top(self, event):
    self.runner.top()
    print("clean the output image")
    self.view.output_view.reset_result_image()


  def load(self, event):
    image_full_file_name = "{}\scan-01.jpg".format(self.cfg.get_input_path())
    cv2image = self.runner.load_image(image_full_file_name) 
    self.view.output_view.set_original_image(cv2image)
