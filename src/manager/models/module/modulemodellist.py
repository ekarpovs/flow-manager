'''
'''

import os
from typing import List, Tuple

from src.manager.models.module.moduleitemmodel import ModuleItemModel

from .modulemodel import ModuleModel


class ModuleModelList():
  def __init__(self, paths: List[str]) -> None:
    self._paths: List[str] = paths
    self._modulemodellist: List[ModuleModel] = []
    self._load()
    return

  @property
  def paths(self) -> str:
    return self._paths

  @property
  def modulemodellist(self) -> List[ModuleModel]:
    return self._modulemodellist

  @modulemodellist.setter
  def modulemodellist(self, model: ModuleModel) -> None:
    self._modulemodellist.append(model)
    return

  def get_modules_by_path(self, path: str) -> List[ModuleModel]:
    models = []
    for model in self.modulemodellist:
      if model.path == path:
        models.append(model)
    return models

  def get_module_or_operation_doc(self, name: str) -> List[str]:
    doc = ''
    if name != '':
      if '.' not in name:
        module = self.get_module_by_name(name)
        doc = [module.doc]
      else:
        operation = self.get_operation_by_name(name)
        doc = operation._doc
    return doc

  @staticmethod
  def _split_name(name: str) -> Tuple[str, str]:
    p = name.split('.')
    mname = p[0]
    oname = p[1]
    return (mname, oname)

  def get_module_by_name(self, name: str) -> ModuleModel:
    for model in self.modulemodellist:
      if model.name == name:
        return model
    return None
  
  def get_operation_by_name(self, name: str) -> ModuleItemModel:
    (mname, oname) = self._split_name(name)
    oper = None
    module = self.get_module_by_name(mname)
    oper = module.get_item(oname)
    return oper

  # Initialization 
  def _load(self) -> None:
    for path in self.paths:
      names = self._names(path)
      for name in names:
        model = ModuleModel(path)
        model.load(name)
        self.modulemodellist = model
    return

  def _names(self, path):
    names = [f[:-3] for f in os.listdir(path)
                  if f.endswith('.py') and f != '__init__.py' and f != 'tester.py']
    return names

