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
