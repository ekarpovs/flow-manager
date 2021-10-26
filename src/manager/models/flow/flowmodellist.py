'''
'''
import os
from typing import List

from flow_model import FlowModel


class FlowModelList():
  def __init__(self, paths: List[str]) -> None:
    self._paths: List[str] = paths
    self._flowmodellist: List[FlowModel] = []
    self._load_worksheets()

  @property
  def flowmodellist(self) -> List[FlowModel]:
    return self._flowmodellist

  @flowmodellist.setter
  def flowmodellist(self, flowmodel: FlowModel) -> None:
    self._flowmodellist.append(flowmodel)
    return
    
  def flowmodel(self, path: str, name: str) -> FlowModel:
    for model in self.flowmodellist:
      if model.path == path and model.name == name:
        return model
    return FlowModel()


  def _worksheets_names(self, path):
    worksheets_names = [f[:-5] for f in os.listdir(path) if f.endswith('.json')]
    return worksheets_names


  def _load_worksheets(self) -> None:
    for path in self._paths:
      ws_names = self._worksheets_names(path)
      for name in ws_names:
        flow_model = FlowModel(path)
        flow_model.load_worksheet(name)
        self.flowmodellist = flow_model
    return

    