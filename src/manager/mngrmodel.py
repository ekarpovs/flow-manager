from typing import Dict, List

from flow_model import FlowModel

from src.manager.models.activeflow.activeflowmodel import ActiveFlowModel

from ..configuration import Configuration
from .models import *

class MngrModel():
  '''
  Fasade for models 
  '''
  def __init__(self, cfg: Configuration):

    self._cfg = cfg
    # Create models
    self._image = ImagesModel()   
    self._flow = None
    self._module = ModuleModelList(self.modules_paths)
    self._worksheet = WorksheetModel(self.worksheets_paths)


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
  def image(self) -> ImagesModel:
    return self._image

# Module
  @property
  def module(self) -> ModuleModelList:
    return self._module

  @property
  def modulemodellist(self) -> List[ModuleModel]:
    return self.module.modulemodellist

# Worksheet
  def worksheetnames(self):
    return self._worksheet.workseetnames
# Flow 
  def create_active_flow_model(self, ws_path: str, ws_name: str, ws: List[Dict]) -> None:
    self._flow = ActiveFlowModel(ws_path, ws_name, ws)
    return

  @property
  def flow(self) -> ActiveFlowModel:
    return self._flow

