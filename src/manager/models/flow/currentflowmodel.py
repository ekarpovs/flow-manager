from copy import copy
from typing import Dict, List

from flow_model import FlowModel, FlowItemModel


class CurrentFlowModel(FlowModel):
  def __init__(self, path: str, name: str, worksheet: List[Dict]) -> None:
    super().__init__(path, name, worksheet)
    # self._active: FlowModel = FlowModel(path, name, worksheet)
    return

  def params_ws(self, name: str) -> Dict:
    params = self.get_item(name).params_ws
    return params
  
  def params_def(self, name: str) -> Dict:
    params = self.get_item(name).params_def
    return params

  def set_params_def(self, name: str, params: Dict) -> None:
    self.get_item(name).params_def = params
    return

  def params(self, name: str) -> Dict:
    params = self.get_item(name).params
    return params

  def set_params(self, name: str, params: Dict) -> None:
    self.get_item(name).params = params
    return


  def names(self) -> List[str]:
    names = []
    for item in self.items:
      name = item.name
      names.append(name)
    return names
  # Merge params