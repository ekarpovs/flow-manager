from tkinter import *
import re
from tkinter.ttk import Combobox
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
    self.columnconfigure(1, weight=1)

    self.param_controls = []


  def set_operation_params(self, params):
    # Clean the view
    [param.grid_forget() for param in self.param_controls]

    for i, param in enumerate(params):
      param_control, param_label = self.controls_factory(param)
      self.param_controls.append(param_control)
      self.param_controls.append(param_label)
      param_control.grid(row=i, column=0, stick=W)
      param_label.grid(row=i, column=1, stick=W)
    
    return

  def controls_factory(self, param):
    # Create control regarding definition --Type:domein...--
    build_data = re.findall('--([^$]*)--', param)[0]
    label_text = param[len(build_data)+4:] 
    param_label = Label(self, text=label_text)
    param_type, param_domain, param_possible_valuess, param_default_value =  build_data.split(':') 
    print("build_data", param_type, param_domain, param_possible_valuess, param_default_value)
    if (param_type == 'n') or (param_type == 'f') or (param_type == 'str'):
      value = IntVar()
      param_control = Entry(self, textvariable=value)
      value.set(param_default_value)
    elif (param_type == 'b'):
      value = BooleanVar()
      param_control = Checkbutton(self, variable=value, onvalue=True, offvalue=False)
      value.set(True)     
    elif (param_type == 's'):
      param_control = Combobox(self, text='')
    else:
      param_control = Label(self, text='unknown param type')

    return param_control, param_label
