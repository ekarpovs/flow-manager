from typing import List

from .models import *
from ..configuration import Configuration


class MngrModel():
  '''
  Fasade for models 
  '''

  def __init__(self, cfg: Configuration):
    self._cfg = cfg
    # Create models
    self._data = DataModel()   
    self._flow =  CurrentFlowModel(self._cfg)
    self._module = ModuleModelList(self.modules_paths)
    # self._worksheet = WorksheetModel(self.worksheets_paths)
    return

  @property
  def modules_paths(self) -> List[str]:
    return self._cfg.modules_paths
  
  # @property
  # def worksheets_paths(self) -> List[str]:
  #   return self._cfg.worksheets_paths

  @property
  def input_paths(self) -> List[str]:
    return self._cfg.input_paths

  @property
  def factory(self):
    return self._cfg.get_factory()

  @property
  def data(self) -> DataModel:
    return self._data

# Module
  @property
  def module(self) -> ModuleModelList:
    return self._module

  @property
  def modulemodellist(self) -> List[ModuleModel]:
    return self.module.modulemodellist

# Flow 
  @property
  def flow(self) -> CurrentFlowModel:
    return self._flow

  def init_flow_model(self, path: str, name: str) -> None:
    self._flow.init_flow_model(path, name)
    return

