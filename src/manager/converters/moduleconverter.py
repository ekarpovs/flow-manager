import re
from typing import Dict, List

from ..models.module import *


class ModuleConverter():
  '''
  Maps data from module model to module view and versa
  '''
  def __init__(self):
    pass

  @staticmethod
  def modulelist_to_module_defs(modulelist: ModuleModelList) -> List[Dict]:
    definitions = []
    paths = modulelist.paths
    for i, path in enumerate(paths):
      iid = f'p{i}'
      list_def = ModuleConverter.list_level_item(iid, path)
      definitions.append(list_def)
      mlist = modulelist.get_modules_by_path(path)
      for j, module in enumerate(mlist):
        module_def = ModuleConverter.module_level_item(iid, str(j), module)
        definitions.append(module_def)
        for n, operation in enumerate(module.items):
          operation_def = ModuleConverter.operation_level_item(module.name, f'{j}.{n}', operation)
          definitions.append(operation_def)
    return definitions

  @staticmethod
  def list_level_item(iid: str, path: str) -> Dict:
    return {"parent": "", "index": "end", "iid": iid, "text": path}

  @staticmethod
  def module_level_item(parent_iid: str, v1: str, module: ModuleModel) -> Dict:
    name = module.name
    doc = module.doc
    return {"parent": parent_iid, "index": "end", "iid": name, "text": name, "values": [v1, doc]}

  @staticmethod
  def operation_level_item(parent_iid: str, v1, operation: ModuleItemModel) -> Dict:
    name = operation.name
    iid = f'{parent_iid}.{name}'
    descr = operation.description
    return {"parent": parent_iid, "index": "end", "iid": iid, "text": name, "values": [v1, descr]}
