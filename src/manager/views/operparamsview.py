from tkinter import *
import re
from tkinter.ttk import Combobox, Checkbutton
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

    self.btn_apply = Button(self, text='Apply', width=BTNW)
    self.btn_reset = Button(self, text='Restet', width=BTNW)


  def clear_operation_params(self):
    for control in self.param_controls:
      control['control'].grid_forget()
      control['label'].grid_forget()
    
    self.param_controls = []

    return


  def set_operation_params(self, params):
    self.clear_operation_params()

    for i, param in enumerate(params):
      param_control, param_label = self.controls_factory(param)
      self.param_controls.append({"control": param_control,"label": param_label})

      param_control.grid(row=i, column=0, padx=PADX, pady=PADY, sticky=W+N)
      param_label.grid(row=i, column=1, padx=PADX, pady=PADY, sticky=W+S)
    
    btns_row = len(self.param_controls)
    if btns_row > 0:
      self.btn_apply['state']=NORMAL
      self.btn_reset['state']=NORMAL
      self.btn_apply.grid(row=btns_row, column=0, padx=PADX, pady=PADY, sticky=W + S)
      self.btn_reset.grid(row=btns_row, column=1, padx=PADX, pady=PADY, sticky=W + S)
    else:
      self.btn_apply['state']=DISABLED
      self.btn_reset['state']=DISABLED

    return

  def collect_operation_params(self):
    params = []
    for control in self.param_controls:
      name = control['label']['text'].split(':')[0]
      if type(control['control']) is Entry: 
        value = control['control'].get()
      elif type(control['control'] is Checkbutton):
        value = control['control'].instate(['selected'])
      else:
        print(type(control['control']))
      
      params.append({"name": name, "value": value})

    return params


  def controls_factory(self, param):
    # Create control regarding definition --Type:domein...--
    build_data = re.findall('--([^$]*)--', param)[0]
    label_text = param[len(build_data)+4:] 
    param_label = Label(self, text=label_text, width=50, anchor=W, justify=LEFT, wraplength=300)
    param_type, param_domain, param_possible_valuess, param_default_value =  build_data.split(':') 

    # Check param_domain
    if (param_type == 'n') or (param_type == 'f') or (param_type == 'str'):
      value = IntVar()
      param_control = Entry(self, textvariable=value)
      value.set(param_default_value)
    elif (param_type == 'b'):
      value = BooleanVar()
      param_control = Checkbutton(self, variable=value, onvalue=True, offvalue=False)
      value.set(param_default_value)
    elif (param_type == 's'):
      param_control = Combobox(self, text='')
    else:
      param_control = Label(self, text='unknown param type')

    return param_control, param_label
