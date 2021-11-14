from typing import List, Dict, Tuple

from src.manager.models.flow.currentflowmodel import CurrentFlowModel



class FlowConverter():
  '''
  Maps data from flow model to flow view and versa
  '''
  def __init__(self):
    pass

  @staticmethod
  def split_ws_name(ws_name) -> Tuple[str, str]:
    name, path = ws_name.split('<')
    name = name[:-1]
    path =  path[:-1]
    return (path, name)
    
  @staticmethod
  def _convert_params_def_to_dict(params_def: List[Dict]) -> Dict:
    def cnv_int(value: str) -> int:
      return int(value)      

    def cnv_float(value: str) -> float:
      return float(value)      

    def cnv_str(value: str) -> str:
      return value      

    def cnv_bool(value: str) -> bool:
      return value == 'True'      

    def cnv_compl():
      return param_def.get('p_types')      



    type_switcher = {
      'int': cnv_int,
      'float': cnv_float,
      'str': cnv_str,
      'bool': cnv_bool,
      'Range': cnv_compl,
      'List': cnv_compl,
      'Dict': cnv_compl
    }

    params = {}
    for param_def in params_def:
      name = param_def.get('name')
      value = param_def.get('default')
      vtype = param_def.get('type')
      converter = type_switcher.get(vtype)
      v = converter(value)   
      params[name] = v
    return params

  @staticmethod
  def _merge_operation_params(params_new: Dict, params_def: List[Dict], params: Dict) -> Dict:
    # Mergre the new param set with current one:
    # for param in new param set:
    #  if a param is in current params set:
    #   if the current param value == new param value:
    #     continue
    #   else:
    #     upate current param value with new one
    #  else:
    #   if the new param value == default param value:
    #     continue
    #   else:
    #     add the pair {param: value} into current param set
    for param_new in params_new:
      name_new = param_new.get('name')
      value_new = param_new.get('value')
      if name_new in params:
        value = params.get(name_new)
        if value_new == value:
          continue
        else:
          params[name_new] = value_new
      else:
        value_def = params_def.get(name_new)
        if value_new == value_def:
          continue
        else:
          params[name_new] = value_new
    return params
