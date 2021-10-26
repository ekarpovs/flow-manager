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
    self.images_model = ImagesModel(self)   
    self._flow_model = FlowModelList(self, self.worksheets_paths)
    self._module_model = ModuleModelLists(self, self.modules_paths)

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
  def modulemodellists(self) -> List[ModuleModelList]:
    return self._module_model._modulemodellists

  def get_modulemodellist(self, path: str) -> ModuleModelList:
    return self._module_model.get_modulemodellist(path)

  @property
  def flowmodellist(self) -> List[FlowModel]:
    return self._flow_model._flowmodellist

  def flowmodel(self, path: str, name: str) -> FlowModel:
    return self._flow_model.flowmodel(path, name)

