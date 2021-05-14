import tkinter as tk
from tkinter import * 
from tkinter.ttk import Combobox, Checkbutton, Spinbox
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

    self.operation_param_controls = {"idx": -1, "exec": "", "param_controls": []}

    self.btn_apply = Button(self, text='Apply', width=BTNW)
    self.btn_save = Button(self, text='Save', width=BTNW)
    self.btn_reset = Button(self, text='Restet', width=BTNW)


  def clear_operation_params(self):
    for control in self.operation_param_controls['param_controls']:
      control['control'].grid_forget()
      control['label'].grid_forget()   
      self.operation_param_controls['idx'] = -1
      self.operation_param_controls['exec'] = ""
      self.operation_param_controls['param_controls'] = []
    return

  def init_operation_params(self, idx, exec):
    self.operation_param_controls["idx"] = idx
    self.operation_param_controls["exec"] = exec
    
    return

  def set_operation_params(self, idx, exec, oper_params):
    self.clear_operation_params()
    self.init_operation_params(idx, exec)

    for i, param in enumerate(oper_params):
      param_control, param_label = self.controls_factory(param)
      self.operation_param_controls['idx'] = idx
      self.operation_param_controls['param_controls'].append({"control": param_control,"label": param_label})

      param_control.grid(row=i, column=0, padx=PADX, pady=PADY, sticky=W+N)
      param_label.grid(row=i, column=1, padx=PADX, pady=PADY, sticky=W+S)
    
    btns_row = len(self.operation_param_controls['param_controls'])
    if btns_row > 0:
      self.btn_apply['state']=NORMAL
      self.btn_save['state']=NORMAL
      self.btn_reset['state']=NORMAL
      self.btn_apply.grid(row=btns_row, column=0, padx=PADX, pady=PADY, sticky=W + S)
      self.btn_save.grid(row=btns_row+1, column=0, padx=PADX, pady=PADY, sticky=W + S)
      self.btn_reset.grid(row=btns_row, column=1, padx=PADX, pady=PADY, sticky=W + S)
    else:
      self.btn_apply['state']=DISABLED
      self.btn_save['state']=DISABLED
      self.btn_reset['state']=DISABLED

    return

  def get_operation_params_item(self):
    params = []
    for control in self.operation_param_controls['param_controls']:
      name = control['label']['text'].split(':')[0]
      if type(control['control']) is Entry:
        entry_value = control['control'].get().strip()
        try:
          if '.' in entry_value:
            value = float(entry_value)
          else:  
            value = int(entry_value)
          # print("Entry value type", type(value))
        except ValueError:
          value = entry_value
      elif type(control['control'] is Checkbutton):
        value = control['control'].instate(['selected'])
      else:
        print("wrong control type", type(control['control']))
      
      params.append({"name": name, "value": value})
      
      operation_params_item = {"idx": self.operation_param_controls['idx'], "exec": self.operation_param_controls['exec'], "params": params}
      
    return operation_params_item


  def controls_factory(self, param):
    # {"type": t, "domain": d, "p_values": pvs, "name": p_name, "value": p_value, "label": l}    
    param_type = param['type']
    param_domain = param['domain']
    param_possible_valuess = param['p_values']
    param_name = param['name']
    param_value = param['value']
    label_text = param['label']

    param_label = Label(self, text=label_text, width=50, anchor=W, justify=LEFT, wraplength=300)

    param_control = self.create_param_control(param)

    # param_control = None
    # # !!!! NEED to Check param_domain !!!
    # if (param_type == 'n') or (param_type == 'f') or (param_type == 'str'):
    #   value = IntVar()
    #   param_control = Entry(self, textvariable=value)
    #   value.set(param_value)
    # elif (param_type == 'b'):
    #   value = BooleanVar()
    #   param_control = Checkbutton(self, variable=value, onvalue=True, offvalue=False)
    #   value.set(param_value)
    # # elif (param_type == 's'):
    # #   param_control = Combobox(self, text='')
    # else:
    #   param_control = Label(self, text='unknown param type')

    return param_control, param_label

  
  def create_param_control(self, param):
    param_domain = param['domain']

    def domain_single(param):

      param_control = Entry(self)
      param_default_value = param['value']     
      item = tk.IntVar()
      item.set(param_default_value)
      param_control.textvariable = item

      return param_control

    def domain_list(param):
      param_control = Entry(self)
      return param_control

    def domain_flag(param):
      param_control = Checkbutton(self)
      return param_control

    #--n;d;[BGR2BGRA:0,BGR2RGB:4,BGR2GRAY:6,BGR2XYZ:32,BGR2YCrCb:36,BGR2HSV:40,BGR2LAB:44,BGR2Luv:50,BGR2HLS:52,BGR2YUV:82];BGR2GRAY-- type: new color space cv2.COLOR_(...)
    def domain_dictionary(param):
      param_control = Combobox(self)

      param_type = param['type']
      # [BGR2BGRA:0,BGR2RGB:4,BGR2GRAY:6,BGR2XYZ:32,BGR2YCrCb:36,BGR2HSV:40,BGR2LAB:44,BGR2Luv:50,BGR2HLS:52,BGR2YUV:82]
      param_possible_values = param['p_values']     
      param_possible_values_dict, param_keys_tuple = self.parse_possible_values_for_dict(param_possible_values)
      param_control['values'] = param_keys_tuple

      param_default_value = param['value']     
      param_control.set(param_default_value)
      selected_item = tk.StringVar()
      param_control.textvariable = selected_item

      return param_control

    def domain_range(param):
      param_control = Spinbox(self)
      return param_control

    domain_switcher = {
      's': domain_single,
      'l': domain_list,
      'd': domain_dictionary,
      'r': domain_range,
      'f': domain_flag
    }

    control_builder = domain_switcher.get(param_domain, 'Invalid domain')

    return control_builder(param)


  @staticmethod
  def parse_possible_values_for_dict(param_possible_values):
    end_idx = len(param_possible_values) - 1
    param_possible_values = param_possible_values[1:end_idx]
    param_possible_values_list = param_possible_values.split(',')
    param_possible_values_dict = {}
    param_key_list = []
    for item in param_possible_values_list:
      k,v = item.split(':')
      param_possible_values_dict[k] = v
      param_key_list.append(k)
    
    param_keys_tuple = tuple(param_key_list)

    return param_possible_values_dict, param_keys_tuple