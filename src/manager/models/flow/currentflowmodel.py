from copy import copy
from typing import Dict, List

from flow_model import FlowModel
from flow_model.flowitemmodel import FlowItemModel
from src.configuration.configuration import Configuration

from src.manager.models import worksheet
from src.manager.models.worksheet.worksheetmodel import WorksheetModel


class CurrentFlowModel():
  def __init__(self, cfg: Configuration) -> None:
    self._ws_model = WorksheetModel(cfg.worksheets_paths)
    self._flow: FlowModel = None
    self._ws_info = None
    return

  @property
  def flow(self) -> FlowModel:
    return self._flow

  def get_item(self, idx: int) -> FlowItemModel:
    return self._flow.get_item(idx)
    
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
    self._ws_info = ws[0]
    return

  def store_flow_model_as_ws(self, path, name) -> None:
    # 1. Buld new ws from flow model
    ws = [self._ws_info]
    for item in self._flow.items:
      iname = item.name
      ws_item = {"exec": iname}
      iparams = item.params
      if len(iparams)> 0:
        ws_item["params"] = iparams
      ialiases = item.aliases
      if len(ialiases)> 0:
        ws_item["aliases"] = ialiases
      ws.append(ws_item)
    self._ws_model.store(path, name, ws)
    return
