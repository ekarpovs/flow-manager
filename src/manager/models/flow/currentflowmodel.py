from copy import copy
from typing import Dict, List, Tuple

from flow_model import FlowModel
from flow_model.flowitemmodel import FlowItemModel

from src.configuration.configuration import Configuration
from src.manager.models.worksheet.worksheetmodel import WorksheetModel


class CurrentFlowModel():
  def __init__(self, cfg: Configuration) -> None:
    self._cfg = cfg
    self._ws_model = WorksheetModel(cfg.worksheets_paths)
    self._flow: FlowModel = None
    return

  @property
  def flow(self) -> FlowModel:
    return self._flow

  @property
  def loaded(self) -> bool:
    return self._flow.loaded

  @property
  def items(self) -> List[FlowItemModel]:
    return self._flow.items

  def reload(self) -> None:
    self._ws_model = WorksheetModel(self._cfg.worksheets_paths)
    return

  def get_item(self, idx: int) -> FlowItemModel:
    return self._flow.get_item(idx)

  def set_item(self, idx: int, item: FlowItemModel) -> None:
    self._flow.set_item(idx, item)
    return

  def remove_item(self, idx) -> None:
    self.flow.remove_item(idx)
    return


  def get_params_ws(self, idx: int) -> Dict:
    params = self._flow.get_item(idx).params_ws
    return params
  
  def get_params_def(self, idx: int) -> Dict:
    params = self._flow.get_item(idx).params_def
    return params

  def set_params_def(self, idx: int, params: Dict) -> None:
    self._flow.get_item(idx).params_def = params
    return

  def get_params(self, idx: int) -> Dict:
    params = self._flow.get_item(idx).params
    return params

  def set_params(self, idx: int, params: Dict) -> None:
    self._flow.get_item(idx).params = params
    return

  def get_names(self) -> List[str]:
    names = [item.name for item in self._flow.items]
    return names

  @property
  def worksheetnames(self) -> List[Dict]:
    return self._ws_model.workseetnames

  def init_flow_model(self, path: str, name: str) -> List[Dict]:
    if path == '' and name == 'new':
      ws = [
              {
                "info": "new worksheet"
              },
              {
                "exec": "glbstm.begin",
                "params": {
                }
              },
              {
                "exec": "glbstm.end"
              }
            ]
    else:
      ws = self._ws_model.read(path, name)
    self._flow = FlowModel(ws)
    return

  def store_flow_model_as_ws(self, path, name) -> Tuple[str, str]:
    ws = self.flow.get_as_ws()
    return self._ws_model.store(path, name, ws)
