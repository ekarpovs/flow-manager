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
    self._flow: CurrentFlowModel = None
    self._module = ModuleModelList(self.modules_paths)
    self._worksheet = WorksheetModel(self.worksheets_paths)
    return

  @property
  def modules_paths(self) -> List[str]:
    return self._cfg.modules_paths
  
  @property
  def worksheets_paths(self) -> List[str]:
    return self._cfg.worksheets_paths

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

# Worksheet
  @property
  def worksheet(self):
    return self._worksheet


  def worksheetnames(self):
    return self._worksheet.workseetnames
# Flow 
  def create_flow_model(self, path: str, name: str) -> None:
    ws = self._worksheet.read(path, name)
    self._flow = CurrentFlowModel(ws)
    return

  @property
  def flow(self) -> CurrentFlowModel:
    return self._flow

