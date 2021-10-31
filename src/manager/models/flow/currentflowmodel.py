from copy import copy
from typing import Dict, List

from flow_model import FlowModel, FlowItemModel


class CurrentFlowModel(FlowModel):
  def __init__(self, worksheet: List[Dict]) -> None:
    super().__init__(worksheet)
    return

  def get_params_ws(self, idx: int) -> Dict:
    params = self.get_item(idx).params_ws
    return params
  
  def get_params_def(self, idx: int) -> Dict:
    params = self.get_item(idx).params_def
    return params

  def set_params_def(self, idx: int, params: Dict) -> None:
    self.get_item(idx).params_def = params
    return

  def get_params(self, idx: int) -> Dict:
    params = self.get_item(idx).params
    return params

  def set_params(self, idx: int, params: Dict) -> None:
    self.get_item(idx).params = params
    return

  def get_names(self) -> List[str]:
    names = [item.name for item in self.items]
    return names
