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
    modules_meta = self.model.modules_model.get_modules_meta()
    modules_meta_conv = self.converter.modules_converter.convert_meta(modules_meta)
    self.view.modules_view.set_modules_meta(modules_meta_conv)

    return


  def update_flows_view(self):
    # TODO: add wrappers to MngrModel & MngrConverter
    self.model.flows_model.load_worksheets_from_all_paths()
    worksheets_names = self.model.flows_model.get_worksheets_names_from_all_paths()
    self.view.flows_view.set_worksheets_names(worksheets_names)

    return


# Actions
  def selected(self, event):
    item = self.view.flows_view.names_combo_box.get()
    path, name = self.converter.flows_converter.split_ws_item(item)
    if path != "":
      flow_meta = self.model.flows_model.get_flow_meta(path, name)
      self.view.flows_view.set_flow_meta(flow_meta)
    else:
      self.view.flows_view.set_flow_meta(self.converter.flows_converter.get_empty_flow())

    return

  def run(self, event):
    self.get_work_sheet()
    self.steps = self.work_sheet['steps']
    # execute the flow
    kwargs = {}
    for step in self.steps:
      print("step", step)
      # load the step's function
      fnc = self.get(step['exec'])
      kwargs = fnc(step, **kwargs)    
    # Call view to select next break point

  
  def step(self, event):
    if self.step_name == None:
      self.get_work_sheet()
      # Temporary
      self.step_name = "clrs.bgrto"

    fnc = self.get(self.step_name)
    print(fnc)
    # Call view to select next step

  def load(self, event):
    cv2image = self.model.load_image()
    self.view.output_view.set_original_image(cv2image)

  def load_mage(self):
    cv2image = self.model.load_image()

    self.view.output_view.set_original_image(cv2image)
