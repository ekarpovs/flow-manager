import tkinter as tk
from tkinter import * 
from tkinter.ttk import Combobox, Spinbox, Button
from ...uiconst import *

class OperParamsView(Frame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 
    self['bd'] = 2
    self['relief'] = RIDGE

    self.grid()
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=2)

    self.operation_param_controls = {"idx": -1, "exec": "", "param_controls": []}

    self.btn_apply = Button(self, text='Apply', width=BTNW)
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
      param_command, param_control, param_label = self.controls_factory(param)
      self.operation_param_controls['idx'] = idx
      self.operation_param_controls['param_controls'].append({"command": param_command, "control": param_control,"label": param_label})

      param_control.grid(row=i, column=0, padx=PADX, pady=PADY, sticky=W+N)
      param_label.grid(row=i, column=1, padx=PADX, pady=PADY, sticky=W+S)
    
    btns_row = len(self.operation_param_controls['param_controls'])
    if btns_row > 0:
      self.btn_apply['state']=NORMAL
      self.btn_reset['state']=NORMAL
    else:
      self.btn_apply['state']=DISABLED
      self.btn_reset['state']=DISABLED
  
    self.btn_apply.grid(row=btns_row, column=0, padx=PADX, pady=PADY, sticky=W + S)
    self.btn_reset.grid(row=btns_row, column=1, padx=PADX, pady=PADY, sticky=W + S)
  
    return

  def get_operation_params_item(self):
    params = []
    for control in self.operation_param_controls['param_controls']:
      name = control['label']['text'].split(':')[0]
      t = type(control['control'])
      if t in [Entry, Combobox, Spinbox, Checkbutton]:
        value = control['command']()
      else:
        print("wrong control type", type(control['control']))
      
      params.append({"name": name, "value": value})
      
      operation_params_item = {"idx": self.operation_param_controls['idx'], "exec": self.operation_param_controls['exec'], "params": params}
      
    return operation_params_item


  def controls_factory(self, param):
    # {"type": t, "domain": d, "p_values": pvs, "name": p_name, "value": p_value, "label": l}    
    param_command, param_control = self.create_param_control(param)

    label_text = param['label']
    param_label = Label(self, text=label_text, width=50, anchor=W, justify=LEFT, wraplength=300)

    return param_command, param_control, param_label

  
  def create_param_control(self, param):
    param_domain = param.get('domain')

    def domain_single(param):
      def get():
        value = param_control.get()
        if param_type == 'f':
          value = float(value)
        elif param_type == 'n':
          value = int(value)
        else:
          pass
        return value

      param_value = param.get('value')
      param_type = param.get('type')
      var = self.get_var_by_type(param_type)  
      var.set(param_value)
      param_control = Entry(self, textvariable=var)
      param_command = get
      return param_command, param_control

    def domain_list(param):
      param_control = Combobox(self)

      def get():
        value = param_control.get()
        if param_type == 'f':
          value = float(value)
        elif param_type == 'n':
          value = int(value)
        else:
          pass
        return value

      param_possible_values = param['p_values']
      param_values_tuple = self.parse_possible_values_list_or_range(param_possible_values)
      param_control['values'] = param_values_tuple

      param_type = param.get('type')
      var = self.get_var_by_type(param_type)  

      param_default_value = param['value']     
      param_control.set(param_default_value)

      param_control.textvariable = var
      param_command = get

      return param_command, param_control

    def domain_flag(param):
      item = tk.BooleanVar()

      def get():
        return item.get()

      param_value = param['value']
      item.set(param_value)

      param_control = Checkbutton(self, variable=item, onvalue=True, offvalue=False, command=get)
      param_command = get

      return param_command, param_control

    def domain_dictionary(param):
      param_control = Combobox(self)

      def get():
        key = param_control.get()
        value = param_dict.get(key, 0)
        return value

      # return key for any value
      def get_key(val):
        for key, value in param_dict.items():
          if val == value:
            return key
        return "key doesn't exist"

      param_type = param['type']
      param_possible_values = param['p_values']     
      param_keys_tuple = self.possible_values_pairs_to_tuple(param_possible_values)
      param_control['values'] = param_keys_tuple
      param_dict = self.possible_values_pairs_to_dict(param_possible_values)
      param_value = param['value']
      if (type(param_value) is int) or (type(param_value) is float):
        param_value = get_key(param_value)

      param_control.set(param_value)
      item = tk.StringVar()
      param_control.textvariable = item
      param_command = get

      return param_command, param_control

    def domain_range(param):
      param_possible_values = param['p_values']
      param_values_tuple = self.parse_possible_values_list_or_range(param_possible_values)
      from_ = param_values_tuple[0]
      to = param_values_tuple[1]

      param_type = param.get('type')
      var = self.get_var_by_type(param_type)  

      def get():
        value = var.get()
        if param_type == 'f':
          value = float(value)
        elif param_type == 'n':
          value = int(value)
        else:
          pass
        return value

      param_value = param['value']     
      var.set(param_value)
      param_control = Spinbox(self, from_=from_, to=to, textvariable=var, wrap=True, command=get)
      param_command = get
      return param_command, param_control

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
  def get_var_by_type(type):
    if type == 'f':
      var = tk.DoubleVar()
    elif type == 'n':
      var = tk.IntVar()
    else:
      var = tk.StringVar()
    return var
  
# Possible parameters values parsing
  # d = [key1:0,key2:1,key3:2]
  # l = [0,1,2]
  # r = [0,10,1]

  @staticmethod
  def split_possible_values_string(param_possible_values):
    end_idx = len(param_possible_values) - 1
    param_possible_values = param_possible_values[1:end_idx]
    return param_possible_values.split(',')

  @staticmethod
  def parse_possible_values_dict_def(param_possible_values):   
    param_possible_values_list = OperParamsView.split_possible_values_string(param_possible_values)
    return [item for  item in param_possible_values_list]


  @staticmethod
  def possible_values_pairs_to_tuple(param_possible_values):   
    pairs_list = OperParamsView.parse_possible_values_dict_def(param_possible_values)
    param_key_list = [item.split(':')[0] for  item in pairs_list]
    param_keys_tuple = tuple(param_key_list)
    return param_keys_tuple

  @staticmethod
  def possible_values_pairs_to_dict(param_possible_values):   
    pairs_list = OperParamsView.parse_possible_values_dict_def(param_possible_values)
    param_dict = {}
    for pair_str in pairs_list:
      kv = pair_str.split(':')
      k = kv[0]
      # v = kv[1]
      v = int(kv[1])
      param_dict[k] = v
    return param_dict

  @staticmethod
  def parse_possible_values_list_or_range(param_possible_values):
    param_possible_values_list = OperParamsView.split_possible_values_string(param_possible_values)
    param_key_list = [item for  item in param_possible_values_list]   
    param_values_tuple = tuple(param_key_list)
    return param_values_tuple
