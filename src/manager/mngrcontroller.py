from .runner import Runner  
from .mngrmodel import MngrModel  
from .mngrconverter import MngrConverter  
from .mngrview import MngrView  

class MngrController():
  def __init__(self, parent):
    self.parent = parent

    print("MNGR-CONTROLLER")

    self.runner = Runner()
    self.model = MngrModel()
    self.converter = MngrConverter()
    self.view = MngrView(self.parent)

    # Bind to flows panel
    self.view.flows_view.names_combo_box.bind('<<ComboboxSelected>>', self.selected)
    self.view.flows_view.btn_load.bind("<Button>", self.load)
    self.view.flows_view.btn_run.bind("<Button>", self.run)
    self.view.flows_view.btn_step.bind("<Button>", self.step)
   
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


  def run(self, event):
    # Move to runner
    self.runner.run_flow(self.flow_meta) 
    # execute the flow
    # Call view to select next break point

  
  def step(self, event):
    pass

  def load(self, event):
    cv2image = self.model.load_image()
    self.view.output_view.set_original_image(cv2image)
