import tkinter as tk
from typing import Dict, List, Tuple

def get_var_by_type(type: str) -> tk.Variable:
  var = tk.StringVar()
  if type == 'float':
    var = tk.DoubleVar()
  elif type == 'int':
    var = tk.IntVar()
  return var

def _convert_to_list_of_dict(params: Dict, params_def: List[Dict]) -> List[Dict]:
  for param_def in params_def:
    name = param_def.get('name')
    pvalue = params.get(name, None)
    if pvalue is not None:
      param_def['default'] = pvalue
  return params_def

def split_possible_values_string(param_possible_values: str) -> List[str]:
  end_idx = len(param_possible_values)
  param_possible_values = param_possible_values[0:end_idx]
  return param_possible_values.split(',')

def parse_possible_values_dict_def(param_possible_values: str) -> List[str]:   
  param_possible_values_list = split_possible_values_string(param_possible_values)
  return [item for  item in param_possible_values_list]

def possible_values_pairs_to_tuple(param_possible_values: List[str]) -> Tuple:   
  pairs_list = parse_possible_values_dict_def(param_possible_values)
  param_key_list = [item.split(':')[0] for  item in pairs_list]
  param_keys_tuple = tuple(param_key_list)
  return param_keys_tuple

def possible_values_pairs_to_dict(param_possible_values: str) -> Dict:   
  pairs_list = parse_possible_values_dict_def(param_possible_values)
  param_dict = {}
  for pair_str in pairs_list:
      kv = pair_str.split(':')
      k = kv[0]
      # v = kv[1]
      v = int(kv[1])
      param_dict[k] = v
  return param_dict

def parse_possible_values_list_or_range(param_possible_values: str) -> Tuple:
  param_possible_values_list = split_possible_values_string(param_possible_values)
  param_key_list = [item for  item in param_possible_values_list]   
  param_values_tuple = tuple(param_key_list)
  return param_values_tuple

def convert_params_def_to_dict(params_def: List[Dict]) -> Dict:
  def _cnv_int(value: str) -> int:
    return int(value)      

  def _cnv_float(value: str) -> float:
    return float(value)      

  def _cnv_str(value: str) -> str:
    return value      

  def _cnv_bool(value: str) -> bool:
    return value == 'True'      

  def _cnv_range(value: str):
    return param_def.get('p_types')      

  def _cnv_scale(value: str):
    p_type = param_def.get('p_types')
    if p_type == 'int':
      return int(value)
    return float(value)     

  def _cnv_list(value: str):
    p_type = param_def.get('p_types')
    if p_type == 'int':
      return int(value)
    if p_type == 'float':
      return float(value)
    return value
        
  def _cnv_dict(value_key: str) -> str:
    p_values_str = param_def.get('p_values')
    p_values_str_pairs = p_values_str.split(',')
    value = None
    for str_pair in p_values_str_pairs:
      str_pair_k_v = str_pair.split(':')
      if value_key in str_pair_k_v:
        value = str_pair_k_v[1].strip()
        break
    p_types = param_def.get('p_types')
    p_types = p_types.split(',')
    if p_types[1] == 'int':
      return int(value)
    return value 

  def _cnv_button(value: str) -> str:
    return value      

  type_switcher = {
    'int': _cnv_int,
    'float': _cnv_float,
    'str': _cnv_str,
    'bool': _cnv_bool,
    'Range': _cnv_range,
    'Scale': _cnv_scale,
    'List': _cnv_list,
    'Dict': _cnv_dict,
    'button': _cnv_button
  }

  params = {}
  for param_def in params_def:
    name = param_def.get('name')
    value = param_def.get('default')
    vtype = param_def.get('type')
    # if vtype == 'button':
    #   continue
    converter = type_switcher.get(vtype)
    v = converter(value)   
    params[name] = v
  return params

