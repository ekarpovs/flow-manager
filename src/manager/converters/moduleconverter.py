import re
from typing import Dict, List

from ..models.module import *


class ModuleConverter():
  '''
  Maps data from module model to module view and versa
  '''
  def __init__(self, parent):
    self.parent = parent 


  def modulelist_to_module_defs(self, modulelist: ModuleModelList) -> List[Dict]:
    definitions = []
    paths = modulelist.paths
    for i, path in enumerate(paths):
      iid = f'p{i}'
      list_def = self.list_level_item(iid, path)
      definitions.append(list_def)
      mlist = modulelist.get_models_by_path(path)
      for j, module in enumerate(mlist):
        module_def = self.module_level_item(iid, str(j), module)
        definitions.append(module_def)
        for n, operation in enumerate(module.items):
          operation_def = self.operation_level_item(module.name, f'{j}.{n}', operation)
          definitions.append(operation_def)
    return definitions

  @staticmethod
  def list_level_item(iid, path: str) -> Dict:
    return {"parent":"", "index":"end", "iid":iid, "text":path}

  @staticmethod
  def module_level_item(parent_iid, v1: str, module: ModuleModel) -> Dict:
    name = module.name
    doc = module.doc
    return {"parent":parent_iid, "index":"end", "iid":name, "text":name, "values": [v1, doc]}

  @staticmethod
  def operation_level_item(parent_iid, v1, operation: ModuleItemModel) -> Dict:
    name = operation.name
    iid = f'{parent_iid}.{name}'
    descr = operation.description
    # return {"parent":parent_iid, "index":"end", "iid":iid, "text":name, "values": [v1, "here will be func __doc__"]}
    return {"parent":parent_iid, "index":"end", "iid":iid, "text":name, "values": [v1, descr]}

  # @staticmethod
  # def parse_single_param_defenition(param_defenition):
  #   # Regarding definition --Type:domein...--
  #   build_data = re.findall('--([^$]*)--', param_defenition)[0]
  #   label_text = param_defenition[len(build_data)+4:] 
  #   param_type, param_domain, param_possible_valuess, param_default_value =  build_data.split(';') 

  #   return param_type, param_domain, param_possible_valuess, param_default_value, label_text


  # @staticmethod
  # def convert_params_defenition_to_params(step, params_defenition, orig_image_size = (0,0)):
  #   oper_params = []
  #   for param_def in params_defenition:
  #     t, d, pvs, df, l = ModulesConverter.parse_single_param_defenition(param_def)
  #     # print("t, d, pvs, df, l", t, d, pvs, df, l)
  #     p_name = l.split(':')[0].strip()
  #     if ('params' in step) and (p_name in step['params']):
  #       p_value = step['params'][p_name]
  #       # print("p_name: p_value", p_name, p_value)
  #     else:
  #       # Check that default value is not either 'h' or 'w' -> convert to real values from image(if exists)
  #       (h, w) = orig_image_size
  #       if (h > 0) and (w > 0):
  #         if df == 'h':
  #           df = h
  #         if df == 'w':
  #           df = w

  #       p_value = df

  #     oper_params.append({"type": t, "domain": d, "p_values": pvs, "name": p_name, "value": p_value, "label": l})
    
  #   if ('params' in step) and ('useorig' in step['params']):
  #     d = 'f'
  #     l = 'useorig: use original image like input'
  #     p_name = 'useorig'
  #     p_value = step['params']['useorig']
  #     oper_params.append({"type": '', "domain": d, "p_values": '', "name": p_name, "value": p_value, "label": l})

  #   return oper_params
