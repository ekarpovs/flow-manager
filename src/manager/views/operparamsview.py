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
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=2)

    self.param_controls = []

    self.btn_save = Button(self, text='Save', width=BTNW)
    self.btn_reset = Button(self, text='Restet', width=BTNW)


  def clear_operation_params(self):
    [param.grid_forget() for param in self.param_controls]
    self.param_controls = []

    return

  def set_operation_params(self, params):
    self.clear_operation_params()

    for i, param in enumerate(params):
      param_control, param_label = self.controls_factory(param)
      self.param_controls.append(param_control)
      self.param_controls.append(param_label)
      # self.rowconfigure(i, weight=1)
      param_control.grid(row=i, column=0, padx=PADX, pady=PADY, sticky=W+N)
      param_label.grid(row=i, column=1, padx=PADX, pady=PADY, sticky=W+S)
    
    btns_row = len(self.param_controls)
    if btns_row > 0:
      self.btn_save['state']=NORMAL
      self.btn_reset['state']=NORMAL
      self.btn_save.grid(row=btns_row, column=0, padx=PADX, pady=PADY, sticky=W + S)
      self.btn_reset.grid(row=btns_row, column=1, padx=PADX, pady=PADY, sticky=W + S)
    else:
      self.btn_save['state']=DISABLED
      self.btn_reset['state']=DISABLED

    return

    

  def controls_factory(self, param):
    # Create control regarding definition --Type:domein...--
    build_data = re.findall('--([^$]*)--', param)[0]
    label_text = param[len(build_data)+4:] 
    param_label = Label(self, text=label_text, width=50, anchor=W, justify=LEFT, wraplength=300)
    param_type, param_domain, param_possible_valuess, param_default_value =  build_data.split(':') 
    # print("build_data", param_type, param_domain, param_possible_valuess, param_default_value)
    # build_data n s [0,4,6,32,36,40,44,50,52,82] 6

    # Check param_domain
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
