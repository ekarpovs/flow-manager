from tkinter import *
from ...uiconst import *

class OperParamsView(LabelFrame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 

    self['bd'] = 2
    self['relief'] = RIDGE
    self['text'] = 'Selected operation parameters'

    self.grid()
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)

    self.param_controls = []


  def set_operation_params(self, params):
    # Clean the view
    [param.grid_forget() for param in self.param_controls]

    for i, param in enumerate(params):
      param_control = self.controls_factory(param)
      self.param_controls.append(param_control)
      self.param_controls[i].grid(row=i, column=0, stick=W)
    
    return

  def controls_factory(self, param):
    # Create control regarding definition --Type:domein...--
    param_control = Label(self, text=param)

    return param_control
