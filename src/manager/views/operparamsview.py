import tkinter as tk
from tkinter import * 
from tkinter.ttk import Combobox, Spinbox, Button
from typing import Callable, Dict, List, Tuple
from ...uiconst import *

class OperParamsView(Frame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 
    # self['bd'] = 2
    # self['relief'] = RIDGE

    self.grid()
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)
    self.columnconfigure(2, weight=1)

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

  def init_operation_params(self, idx, item_name):
    self.operation_param_controls["idx"] = idx
    self.operation_param_controls["exec"] = item_name
    
    return

  @staticmethod
  def _convert_to_list_of_dict(params: Dict, params_def: List[Dict]) -> List[Dict]:
    for param_def in params_def:
      name = param_def.get('name')
      pvalue = params.get(name, None)
      if pvalue is not None:
        param_def['default'] = pvalue
    return params_def

  def set_operation_params_from_dict(self, idx: int, item_name: str, params: Dict, params_def: List[Dict]) -> None:
    params_list = self._convert_to_list_of_dict(params, params_def)
    self.set_operation_params(idx, item_name, params_list)
    return

  def set_operation_params(self, idx, item_name: str, oper_params: List[Dict]) -> None:
    self.clear_operation_params()
    self.init_operation_params(idx, item_name)
    self.btn_apply['state']=DISABLED
    self.btn_reset['state']=DISABLED 
    self.btn_apply.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W+N)
    self.btn_reset.grid(row=0, column=2, padx=PADX, pady=PADY, sticky=W+N)

    for i, param in enumerate(oper_params):
      param_command, param_control, param_label = self.controls_factory(param)
      self.operation_param_controls['idx'] = idx
      self.operation_param_controls['param_controls'].append({"command": param_command, "control": param_control,"label": param_label})

      param_control.grid(row=i+1, column=0, padx=PADX, pady=PADY, sticky=W+N)
      param_label.grid(row=i+1, column=1, columnspan=2, padx=PADX, pady=PADY, sticky=W+S)

    if len(oper_params) > 0:
      self.btn_apply['state']=NORMAL
      self.btn_reset['state']=NORMAL    
    return

  def get_operation_params_item(self) -> List[Dict]:
    params = []
    for control in self.operation_param_controls['param_controls']:
      name = control['label']['text'].split('-')[0].strip()
      t = type(control['control'])
      if t in [Entry, Combobox, Spinbox, Checkbutton]:
        value = control['command']()
      else:
        print("wrong control type", type(control['control']))    
      params.append({"name": name, "value": value})     
    return params


  def controls_factory(self, param):
    # {"type": t, "domain": d, "p_values": pvs, "name": p_name, "value": p_value, "label": l}    
    param_command, param_control = self.create_param_control(param)
    name = param.get('name')
    comment = param.get('comment')
    label_text = f"{name} - {comment})"
    param_label = Label(self, text=label_text, width=50, anchor=W, justify=LEFT, wraplength=300)

    return param_command, param_control, param_label

  
  def create_param_control(self, param: Dict) -> Tuple[Callable, Entry]:   
    # 'name':'y0'
    # 'type':'int'
    # 'default':'0'
    # 'p_values':None
    # 'comment':'left top coordinate'

    # 'name':'thrs1'
    # 'type':'Range[int]'
    # 'default':'50'
    # 'p_values':'10,150,1'
    # 'comment':'threshold1'
    
    # 'name':'type'
    # 'comment':'new color space, one from cv2.COLOR_(...)'
    # 'p_values':'BGR2BGRA:0,BGR2RGB:4,BGR2GRAY:6,BGR2XYZ:32,BGR2YCrCb:36,BGR2HSV:40,BGR2LAB:44,BGR2Luv:50,BGR2HLS:52,BGR2YUV:82'
    # 'default':'BGR2GRAY'
    # 'type':'Dict[str,int]'

    # 'name':'kernel'
    # 'comment':'kernel size'
    # 'p_values':'3,5,7,9'
    # 'default':'3'
    # 'type':'List[int]'

    param_type = param.get('type')

    def pint(param: Dict) -> Tuple[Callable, Entry]:
      def get():
        return int(param_control.get())

      param_value = param.get('default')
      var = tk.IntVar()
      var.set(param_value)
      param_control = Entry(self, textvariable=var)
      param_command = get
      return param_command, param_control

    def pfloat(param: Dict) -> Tuple[Callable, Entry]:
      def get():
        return float(param_control.get())

      param_value = param.get('default')
      var = tk.DoubleVar()
      var.set(param_value)
      param_control = Entry(self, textvariable=var)
      param_command = get
      return param_command, param_control

    def pstr(param: Dict) -> Tuple[Callable, Entry]:
      def get():
        return param_control.get()

      param_value = param.get('default')
      var = tk.StringVar()
      var.set(param_value)
      param_control = Entry(self, textvariable=var)
      param_command = get
      return param_command, param_control

    def pbool(param: Dict) -> Tuple[Callable, Checkbutton]:
      item = tk.BooleanVar()
      def get():
        return item.get()
      param_value = param['value']
      item.set(param_value)
      param_control = Checkbutton(self, variable=item, onvalue=True, offvalue=False, command=get)
      param_command = get
      return param_command, param_control

    def plist(param: Dict) -> Tuple[Callable, Combobox]:
      p_types = param.get('p_types')
      param_control = Combobox(self)
      def get():
        value = param_control.get()
        if p_types == 'float':
          value = float(value)
        elif p_types == 'int':
          value = int(value)
        else:
          pass
        return value

      param_possible_values = param.get('p_values')
      param_values_tuple = self.parse_possible_values_list_or_range(param_possible_values)
      param_control['values'] = param_values_tuple
      var = self.get_var_by_type(p_types)  
      param_default_value = param.get('default')    
      param_control.set(param_default_value)
      param_control.textvariable = var
      param_command = get
      return param_command, param_control


    def pdict(param: Dict) -> Tuple[Callable, Combobox]:
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

      p_types = param.get('p_types')
      param_possible_values = param.get('p_values')     
      param_keys_tuple = self.possible_values_pairs_to_tuple(param_possible_values)
      param_control['values'] = param_keys_tuple
      param_dict = self.possible_values_pairs_to_dict(param_possible_values)
      param_default_value = param.get('default')
      if (type(param_default_value) is int) or (type(param_default_value) is float):
        param_default_value = get_key(param_default_value)
      param_control.set(param_default_value)
      item = tk.StringVar()
      param_control.textvariable = item
      param_command = get
      return param_command, param_control

    def prange(param: Dict) -> Tuple[Callable, Spinbox]:
      param_possible_values = param.get('p_values')
      param_values_tuple = self.parse_possible_values_list_or_range(param_possible_values)
      from_ = param_values_tuple[0]
      to = param_values_tuple[1]
      p_types = param.get('p_types')
      var = self.get_var_by_type(p_types)  

      def get():
        value = var.get()
        if p_types == 'float':
          value = float(value)
        elif p_types == 'int':
          value = int(value)
        else:
          pass
        return value

      param_default_value = param.get('default')     
      var.set(param_default_value)
      param_control = Spinbox(self, from_=from_, to=to, textvariable=var, wrap=True, command=get)
      param_command = get
      return param_command, param_control


    type_switcher = {
      'int': pint,
      'float': pfloat,
      'str': pstr,
      'bool': pbool,
      'Dict': pdict,
      'List': plist,
      'Range': prange
    }

    control_builder = type_switcher.get(param_type, 'Invalid type')

    return control_builder(param)



    # def domain_range(param):
    #   param_possible_values = param['p_values']
    #   param_values_tuple = self.parse_possible_values_list_or_range(param_possible_values)
    #   from_ = param_values_tuple[0]
    #   to = param_values_tuple[1]

    #   param_type = param.get('type')
    #   var = self.get_var_by_type(param_type)  

    #   def get():
    #     value = var.get()
    #     if param_type == 'f':
    #       value = float(value)
    #     elif param_type == 'n':
    #       value = int(value)
    #     else:
    #       pass
    #     return value

    #   param_value = param['value']     
    #   var.set(param_value)
    #   param_control = Spinbox(self, from_=from_, to=to, textvariable=var, wrap=True, command=get)
    #   param_command = get
    #   return param_command, param_control

    # type_switcher = {
    #   'int': pint,
    #   'float': pfloat,
    #   'str': pstr,
    #   'Dict': pdict,
    #   'List': plist,
    #   'Range': prange
    # }

    # control_builder = type_switcher.get(param_type, 'Invalid domain')

    # return control_builder(param)

  @staticmethod
  def get_var_by_type(type) -> Variable:
    if type == 'float':
      var = tk.DoubleVar()
    elif type == 'int':
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
    end_idx = len(param_possible_values)
    param_possible_values = param_possible_values[0:end_idx]
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
