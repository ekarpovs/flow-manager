# from tkinter import filedialog as fd
from typing import List
from flow_model import FlowModel
from .models import *
from .models.flow import FlowModelList
from ..configuration import Configuration

class MngrModel():
  def __init__(self, cfg: Configuration):

    self._cfg = cfg
    # Create models
    self.modules_model = ModulesModel(self)
    # self.flows_model = FlowsModel(self)
    self.images_model = ImagesModel(self)
    self._flows_model = FlowModelList(self, self.worksheets_paths)

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
  def flowmodellist(self) -> List[FlowModel]:
    return self._flows_model._flowmodellist

  def flowmodel(self, path: str, name: str) -> FlowModel:
    return self._flows_model.flowmodel(path, name)
