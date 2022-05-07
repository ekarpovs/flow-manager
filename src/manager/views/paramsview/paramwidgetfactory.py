import tkinter as tk
from tkinter import * 
from tkinter.ttk import Combobox, Spinbox, Button
from typing import Callable, Dict, List, Tuple

from .paramsutils import *
from ....uiconst import *


class ParamWidgetFactory():
  def __init__(self):
    self._container = None
    return

  @property
  def container(self) -> Widget:
    return self._container
  
  @container.setter
  def container(self, _container) -> None:
    self._container = _container

  def create(self, param_def: Dict) -> Tuple[Callable, Callable, Widget]:
    param_type = param_def.get('type')

    type_switcher = {
      'int': self._create_entry,
      'float': self._create_entry,
      'str': self._create_entry,
      'bool': self._create_check,
      'Dict': self._create_combo,
      'List': self._create_combo,
      'Range': self._create_spin,
      'Scale': self._create_scale
    }

    widget_builder = type_switcher.get(param_type, 'Invalid type')
    return widget_builder(param_def)

  def _create_entry(self, param_def: Dict) -> Tuple[Callable, Callable, Entry]:
    def get():
      value = wd.get()
      if p_type == 'float':
        value = float(value)
      elif p_type == 'int':
        value = int(value)
      else:
        pass
      return value

    def set(value):
      var.set(value)
      return
    width=10
    p_type = param_def.get('type')
    p_name = param_def.get('name')
    p_value = param_def.get('default')
    var = None
    if p_type == 'int':
      var = tk.IntVar()
    elif p_type == 'float':
      var = tk.DoubleVar()
    else:
      var = tk.StringVar()
      width=50

    var.set(p_value)
    wd = Entry(self._container, name=p_name,textvariable=var, width=width)
    return get, set, wd

  def _create_check(self, param_def) -> Tuple[Callable, Callable, Checkbutton]:
    def get() -> bool:
      return var.get()

    def set(value: bool):
      wd.set = value
      return
    p_name = param_def.get('name')
    p_value = param_def.get('default')
    var = tk.BooleanVar()
    var.set(p_value)
    wd = Checkbutton(self._container, name=p_name, variable=var, onvalue=True, offvalue=False, command=get)
    return get, set, wd

  def _create_combo(self, param_def) -> Tuple[Callable, Callable, Combobox]:
    def get_d():
      key = wd.get()
      value = p_dict.get(key, 0)
      return value

    def get_l():
      value = wd.get()
      if p_types == 'float':
        value = float(value)
      elif p_types == 'int':
        value = int(value)
      else:
        pass
      return value

    def set(value):
      if p_type == 'Dict':
        wd.set(get_key(value))
      else:
        wd.set()
      return

    def get_key(val):
      for key, value in p_dict.items():
        if val == value:
          return key
      return "key doesn't exist"

    p_type = param_def.get('type')
    p_name = param_def.get('name')   
    p_types = param_def.get('p_types')
    p_possible_values = param_def.get('p_values')
    p_default_value = param_def.get('default')
    p_values_tuple = possible_values_pairs_to_tuple(p_possible_values)
    if p_type == 'Dict':
      p_dict = possible_values_pairs_to_dict(p_possible_values)
      if (type(p_default_value) is int) or (type(p_default_value) is float):
        p_default_value = get_key(p_default_value)
      var = tk.StringVar()
      getter = get_d
    else: # List
      var = get_var_by_type(p_types)  
      getter = get_l
    
    wd = Combobox(self._container, name=p_name, width=10)
    wd['values'] = p_values_tuple
    wd.set(p_default_value)
    wd.textvariable = var
    setter = set
    return getter, setter, wd

  def _create_spin(self, param_def) -> Tuple[Callable, Callable, Spinbox]:
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
      wd.set(value)
      return

    p_type = param_def.get('type')
    p_name = param_def.get('name')
    p_types = param_def.get('p_types')
    p_possible_values = param_def.get('p_values')
    p_default_value = param_def.get('default')
    p_values_tuple = parse_possible_values_list_or_range(p_possible_values)
    from_ = p_values_tuple[0]
    to = p_values_tuple[1]
    resolution = p_values_tuple[2]
    var = get_var_by_type(p_types)  
    var.set(p_default_value)
    wd = Spinbox(self, name=p_name, from_=from_, to=to, textvariable=var, wrap=True, command=get)
    return get, set, wd

  def _create_scale(self, param_def) -> Tuple[Callable, Callable, Scale]:
    def get():
      value = wd.get()
      r = value %2
      if r == 0:
        value += increment
      if p_types == 'int':
        return int(value)
      return float(value)

    def set(value):
      if p_types == 'int':
        wd.set(int(value))
      else:
        wd.set(float(value))
      return

    p_type = param_def.get('type')
    p_name = param_def.get('name')
    p_types = param_def.get('p_types')
    p_possible_values = param_def.get('p_values')
    p_default_value = param_def.get('default')
    p_values_tuple = parse_possible_values_list_or_range(p_possible_values)
    if p_types == 'float':
      from_ = float(p_values_tuple[0])
      to = float(p_values_tuple[1])
      resolution = float(p_values_tuple[2])
      increment = float(p_values_tuple[3])
    elif p_types == 'int':
      from_ = int(p_values_tuple[0])
      to = int(p_values_tuple[1])
      resolution = int(p_values_tuple[2])
      increment = float(p_values_tuple[3])
    else:
      pass      
    var = get_var_by_type(p_types)  
    var.set(p_default_value)
    wd = Scale(self._container, name=p_name,from_=from_, to=to, resolution=resolution, variable=var, length=250, orient=HORIZONTAL)
    return get, set, wd

