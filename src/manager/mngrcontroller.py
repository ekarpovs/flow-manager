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

    return


  def update_modules_view(self):
    # TODO: add wrappers to MngrModel & MngrConverter
    modules_meta = self.model.modules_model.get_modules_meta()
    modules_meta_conv = self.converter.modules_converter.convert_meta(modules_meta)
    self.view.modules_view.set_modules_meta(modules_meta_conv)

    return


  def update_flows_view(self):
    # TODO: add wrappers to MngrModel & MngrConverter
    flows_meta = self.model.flows_model.get_flows_meta()
    # flows_meta_conv = self.converter.flows_converter.convert_meta(modules_meta)
    # self.view.flows_view.set_flows_meta(flows_meta_conv)

    return

# # Meta data
#   def get_all(self):
#     self.get_modules_meta()
#     # self.get_work_sheet_names()

#     return

#   def get_modules_meta(self):
#     self.modules_meta = self.model.get_modules_meta()

#     return

#   def get_work_sheet_names(self):
#     self.work_sheet_names = self.model.get_work_sheet_names()


#   def get_work_sheet(self):
#     if self.work_sheet_name != None:
#       self.work_sheet = self.model.get_work_sheet()
#       print("contr", self.work_sheet)
  

#   def show_all(self):
#     self.show_modules_meta()
#     self.show_work_sheet_names()

#     return


#   def show_modules_meta(self):
#     self.view.show_modules_meta(self.modules_meta)

#     return

#   def show_work_sheet_names(self):
#     self.view.show_work_sheet_names(self.work_sheet_names)


#   # def show_work_sheet(self):
#   #   self.view.show_work_sheet(self.work_sheet)

#     return


# Actions
  def selected(self, event):
    self.work_sheet_name = self.view.flows_view.names_combo_box.get()
    print("selected", self.work_sheet_name)
    self.model.load_work_sheet(self.work_sheet_name)

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
