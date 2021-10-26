from typing import List

from ..configuration import Configuration
from flow_model import FlowModel

from .models import *

class MngrModel():
  '''
  Fasade for models 
  '''
  def __init__(self, cfg: Configuration):

    self._cfg = cfg
    # Create models
    self._image = ImagesModel()   
    self._flow = FlowModelList(self.worksheets_paths)
    self._module = ModuleModelList(self.modules_paths)

  @property
  def modules_paths(self):
    return self._cfg.modules_paths
  
  @property
  def worksheets_paths(self):
    return self._cfg.worksheets_paths

  @property
  def input_paths(self):
    return self._cfg.input_paths

  @property
  def factory(self):
    return self._cfg.get_factory()

  @property
  def image(self):
    return self._image

# Module
  @property
  def module(self):
    return self._module

  @property
  def modulemodellist(self) -> List[ModuleModel]:
    return self.module.modulemodellist

  # def get_modulemodellist(self, path: str) -> ModuleModelList:
  #   return self._module.get_modulemodellist(path)

  # def get_modulemodel(self, path: str, name) -> ModuleModel:
  #   return self._module.get_modulemodellist(path).get_model(path, name)

  # def get_moduleitemmodel(self, path: str, name, iname) -> ModuleItemModel:
  #   return self.get_modulemodel(path, name).get_item(iname)

# Flow 
  @property
  def flow(self):
    return self._flow

  @property
  def flowmodellist(self) -> List[FlowModel]:
    return self.flow.flowmodellist

  def flowmodel(self, path: str, name: str) -> FlowModel:
    return self.flow.flowmodel(path, name)

