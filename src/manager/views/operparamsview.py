import tkinter as tk
from tkinter import * 
from tkinter.ttk import Combobox, Spinbox, Button
from typing import Callable, Dict, List, Tuple

# from ...mix.incscale import IncScale
from ...uiconst import *

class OperParamsView(Frame):
  def __init__(self, parent) -> None:
    super().__init__(parent)
    self.parent = parent 
    # self['bd'] = 2
    # self['relief'] = RIDGE

    self.grid()
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)
    self.columnconfigure(2, weight=1)

    self.buttons_frame = Frame(self)
    self.buttons_frame.grid(row=0, column=0, columnspan=3, padx=PADX, pady=PADY, sticky=W+N+E)
    self.btn_apply = Button(self.buttons_frame, text='Apply', width=BTNW_S)
    self.btn_reset = Button(self.buttons_frame, text='Reset', width=BTNW_S)
    self.btn_default = Button(self.buttons_frame, text='Default', width=BTNW_S)
    self.btn_apply.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W+N)
    self.btn_reset.grid(row=0, column=1, padx=PADX, pady=PADY, sticky=W+N)
    self.btn_default.grid(row=0, column=2, padx=PADX, pady=PADY, sticky=W+N)

    self.operation_param_controls = {"idx": -1, "exec": "", "param_controls": []}
    self.btn_apply['state']=DISABLED
    self.btn_default['state']=DISABLED
    self.btn_reset['state']=DISABLED
    return

# API
  def create_operation_params_controls(self, idx: int, item_name: str, params: Dict, params_def: List[Dict]) -> None:
    self._clear_operation_params()
    params_list = self._convert_to_list_of_dict(params, params_def)
    self._create_controls(idx, item_name, params_list)
    return

  def get_current_opreation_params_idx(self) -> int:
    return self.operation_param_controls.get('idx')

  def get_current_operation_param_control(self, cname) -> Widget:   
    for control in self.operation_param_controls['param_controls']:
      name = control['label']['text'].split('-')[0].strip()
      if cname == name:
        return control['control']
    return None

  def get_current_operation_params_def(self) -> Dict:
    params = {}
    for control in self.operation_param_controls['param_controls']:
      name = control['label']['text'].split('-')[0].strip()
      t = type(control['control'])
      if t in [Entry, Combobox, Spinbox, Checkbutton, Button, Scale]:
        value = control['getter']()
      else:
        print("wrong control type", type(control['control']))    
      # params.append({"name": name, "value": value})     
      params[name] =  value     
    return params


# Local methods
  def _clear_operation_params(self) -> None:
    for control in self.operation_param_controls['param_controls']:
      control['control'].grid_forget()
      control['label'].grid_forget()   
    self.operation_param_controls['idx'] = -1
    self.operation_param_controls['exec'] = ''
    self.operation_param_controls['param_controls'] = []
    return

  def _init_operation_params(self, idx: int, item_name: str) -> None:
    self.operation_param_controls["idx"] = idx
    self.operation_param_controls["exec"] = item_name
    return

  def _create_controls(self, idx, item_name: str, oper_params: List[Dict]) -> None:
    self.btn_apply['state']=NORMAL
    self.btn_default['state']=NORMAL
    self.btn_reset['state']=NORMAL

    self._init_operation_params(idx, item_name)

    for i, param in enumerate(oper_params):
      param_getter, param_setter, param_control, param_label = self._controls_factory(param)
      self.operation_param_controls['idx'] = idx
      # self.params_controls[param.get('name')] = param_control
      self.operation_param_controls['param_controls'].append({
        "getter": param_getter, "setter": param_setter, "control": param_control,"label": param_label
        })

      param_control.grid(row=i+1, column=0, padx=PADX, pady=PADY, sticky=W+N)
      param_label.grid(row=i+1, column=1, columnspan=2, padx=PADX, pady=PADY, sticky=W+S)
    if len(oper_params) == 0:
      self.btn_default['state']=DISABLED
      self.btn_reset['state']=DISABLED
    return

  def _controls_factory(self, param: Dict) -> Tuple[Callable, Callable, Widget, Label]:
    # {"type": t, "domain": d, "p_values": pvs, "name": p_name, "value": p_value, "label": l}    
    param_getter, param_setter, param_control = self._create_control(param)
    name = param.get('name')
    comment = param.get('comment')
    label_text = f"{name} - {comment}"
    param_label = Label(self, text=label_text, width=50, anchor=W, justify=LEFT, wraplength=300)
    return param_getter, param_setter, param_control, param_label

  def _create_control(self, param: Dict) -> Tuple[Callable, Callable, Widget]:   
    param_type = param.get('type')

    def _pint(param: Dict) -> Tuple[Callable, Callable, Entry]:
      def get():
        return int(param_control.get())
      
      def set(value: int):
        param_control.set(value)

      param_value = param.get('default')
      var = tk.IntVar()
      var.set(param_value)
      param_control = Entry(self, textvariable=var)
      param_getter = get
      param_setter = set
      return param_getter, param_setter, param_control

    def _pfloat(param: Dict) -> Tuple[Callable, Callable, Entry]:
      def get():
        return float(param_control.get())

      def set(value: float):
        param_control.set(value)

      param_value = param.get('default')
      var = tk.DoubleVar()
      var.set(param_value)
      param_control = Entry(self, textvariable=var)
      param_getter = get
      param_setter = set
      return param_getter, param_setter, param_control

    def _pstr(param: Dict) -> Tuple[Callable, Callable, Entry]:
      def get():
        return param_control.get()

      def set(value: str):
        var.set(value)

      param_value = param.get('default')
      var = tk.StringVar()
      var.set(param_value)
      param_control = Entry(self, textvariable=var)
      param_getter = get
      param_setter = set
      return param_getter, param_setter, param_control

    def _pbool(param: Dict) -> Tuple[Callable, Callable, Checkbutton]:
      item = tk.BooleanVar()
      def get():
        return item.get()

      def set(value: bool):
        param_control.set(value)

      param_value = param.get('default')
      item.set(param_value)
      param_control = Checkbutton(self, variable=item, onvalue=True, offvalue=False, command=get)
      param_getter = get
      param_setter = set
      return param_getter, param_setter, param_control

    def _plist(param: Dict) -> Tuple[Callable, Callable, Combobox]:
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

      def set(value):
        param_control.set(value)

      param_possible_values = param.get('p_values')
      param_values_tuple = self.parse_possible_values_list_or_range(param_possible_values)
      param_control['values'] = param_values_tuple
      var = self.get_var_by_type(p_types)  
      param_default_value = param.get('default')    
      param_control.set(param_default_value)
      param_control.textvariable = var
      param_getter = get
      param_setter = set
      return param_getter, param_setter, param_control

    def _pdict(param: Dict) -> Tuple[Callable, Callable, Combobox]:
      param_control = Combobox(self)

      def get():
        key = param_control.get()
        value = param_dict.get(key, 0)
        return value

      def set(value):
        param_control.set(value)

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
      param_getter = get
      param_setter = set
      return param_getter, param_setter, param_control

    def _prange(param: Dict) -> Tuple[Callable, Callable, Spinbox]:
      param_possible_values = param.get('p_values')
      param_values_tuple = self.parse_possible_values_list_or_range(param_possible_values)
      from_ = param_values_tuple[0]
      to = param_values_tuple[1]
      resolution = param_values_tuple[2]
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

      def set(value):
        param_control.set(value)

      param_default_value = param.get('default')     
      var.set(param_default_value)
      param_control = Spinbox(self, from_=from_, to=to, textvariable=var, wrap=True, command=get)
      param_getter = get
      param_setter = set
      return param_getter, param_setter, param_control

    def _pscale(param: Dict) -> Tuple[Callable, Callable, Scale]:
      param_possible_values = param.get('p_values')
      param_values_tuple = self.parse_possible_values_list_or_range(param_possible_values)
      p_types = param.get('p_types')
      if p_types == 'float':
        from_ = float(param_values_tuple[0])
        to = float(param_values_tuple[1])
        resolution = float(param_values_tuple[2])
        increment = float(param_values_tuple[3])
      elif p_types == 'int':
        from_ = int(param_values_tuple[0])
        to = int(param_values_tuple[1])
        resolution = int(param_values_tuple[2])
        increment = float(param_values_tuple[3])
      else:
        pass      
      var = self.get_var_by_type(p_types)  

      def get():
        # x, y = param_control.coords()
        # clicked = param_control.identify(x, y)
        value = param_control.get()
        r = value %2
        if r == 0:
          value += increment
        # param_control.set(value)
        if p_types == 'int':
          return int(value)
        return float(value)

      def set(value):
        if p_types == 'int':
          param_control.set(int(value))
        else:
          param_control.set(float(value))
        return

      param_default_value = param.get('default')     
      var.set(param_default_value)
      param_control = Scale(self, from_=from_, to=to, resolution=resolution, variable=var, length=170, orient=HORIZONTAL)
      # param_control = IncScale(self, from_=from_, to=to, resolution=resolution, increment=increment, variable=var, length=170, orient=HORIZONTAL)
      param_getter = get
      param_setter = set
      return param_getter, param_setter, param_control

    def _pbutton(param: Dict) -> Tuple[Callable, Callable, Button]:
      def get():
        return param_value

      def set(value):
        return

      param_value = param.get('default')
      param_control = Button(self, text=param_value, width=BTNW_S)
      param_getter = get
      param_setter = set
      return param_getter, param_setter, param_control

    type_switcher = {
      'int': _pint,
      'float': _pfloat,
      'str': _pstr,
      'bool': _pbool,
      'Dict': _pdict,
      'List': _plist,
      'Range': _prange,
      'Scale': _pscale,
      'button': _pbutton
    }

    control_builder = type_switcher.get(param_type, 'Invalid type')
    return control_builder(param)

# Class utilities, converters
  @staticmethod
  def get_var_by_type(type: str) -> Variable:
    var = tk.StringVar()
    if type == 'float':
      var = tk.DoubleVar()
    elif type == 'int':
      var = tk.IntVar()
    return var

  @staticmethod
  def _convert_to_list_of_dict(params: Dict, params_def: List[Dict]) -> List[Dict]:
    for param_def in params_def:
      name = param_def.get('name')
      pvalue = params.get(name, None)
      if pvalue is not None:
        param_def['default'] = pvalue
    return params_def

  @staticmethod
  def split_possible_values_string(param_possible_values: str) -> List[str]:
    end_idx = len(param_possible_values)
    param_possible_values = param_possible_values[0:end_idx]
    return param_possible_values.split(',')

  @staticmethod
  def parse_possible_values_dict_def(param_possible_values: str) -> List[str]:   
    param_possible_values_list = OperParamsView.split_possible_values_string(param_possible_values)
    return [item for  item in param_possible_values_list]

  @staticmethod
  def possible_values_pairs_to_tuple(param_possible_values: List[str]) -> Tuple:   
    pairs_list = OperParamsView.parse_possible_values_dict_def(param_possible_values)
    param_key_list = [item.split(':')[0] for  item in pairs_list]
    param_keys_tuple = tuple(param_key_list)
    return param_keys_tuple

  @staticmethod
  def possible_values_pairs_to_dict(param_possible_values: str) -> Dict:   
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
  def parse_possible_values_list_or_range(param_possible_values: str) -> Tuple:
    param_possible_values_list = OperParamsView.split_possible_values_string(param_possible_values)
    param_key_list = [item for  item in param_possible_values_list]   
    param_values_tuple = tuple(param_key_list)
    return param_values_tuple
