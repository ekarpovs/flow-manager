'''
'''

import os
from typing import List

from .modulemodel import ModuleModel


class ModuleModelList():
  def __init__(self, path: str) -> None:
    self._path: str = path
    self._modulemodellist: List[ModuleModel] = []
    return

  @property
  def path(self) -> str:
    return self._path

  @property
  def modulemodellist(self) -> List[ModuleModel]:
    return self._modulemodellist

  @modulemodellist.setter
  def modulemodellist(self, model: ModuleModel) -> None:
    self._modulemodellist.append(model)
    return


  def get_model(self, path: str, name: str) -> ModuleModel:
    for model in self.modulemodellist:
      if model.path == path and model.name == name:
        return model
    return ModuleModel()
  

  # Initialization 
  def load(self) -> None:
    names = self._names(self._path)
    for name in names:
      model = ModuleModel(self._path)
      model.load(name)
      self.modulemodellist = model
    return


  # Initialization 
  def _names(self, path):
    names = [f[:-3] for f in os.listdir(path)
                  if f.endswith('.py') and f != '__init__.py' and f != 'tester.py']
    return names

