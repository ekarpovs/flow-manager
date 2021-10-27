from copy import copy
from typing import Dict, List

from flow_model import FlowModel, FlowItemModel


class ActiveFlowModel():
  def __init__(self, path: str, name: str, worksheet: List[Dict]) -> None:
    self._active: FlowModel = FlowModel(path, name, worksheet)
    self._default_params: Dict = None
    self._active_params: Dict = None #copy.deepcopy(self._item.params)
    return

  @property
  def active(self) -> FlowModel:
    return self._active

  @property
  def default_params(self) -> Dict:
    return self._default_params
  
  @default_params.setter
  def default_params(self, params: Dict) -> None:
    self._default_params = params

  def names(self) -> List[str]:
    names = []
    for item in self.active.items:
      name = item.name
      names.append(name)
    return names
  # Merge params