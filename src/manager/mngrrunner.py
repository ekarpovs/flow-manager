from typing import Dict, List, Tuple

from flow_model import FlowModel
from flow_runner import Runner
from flow_converter import FlowConverter
from flow_storage import FlowStorage, FlowDataType

from ..configuration import Configuration

class MngrRunner():
  '''
  Flow runner client
  '''
  
  def __init__(self, cfg: Configuration) -> None:
    self._cfg = cfg
    self._runner = Runner()
    self._storage = None
    return

  @property
  def runner(self) -> Runner:
    return self._runner

  @property
  def storage(self) -> FlowStorage:
    return self._storage

  @property
  def initialized(self) -> bool:
    return self.runner.initialized

  @property
  def state_idx(self) -> int:
    return self.runner.state_idx

  @property
  def output_from_state(self) -> str:
    return self.runner._output_from_state

  def build(self, model: FlowModel) -> None:
    if self._storage is not None:
      self._storage.close()
    self._storage = FlowStorage(self._cfg.cfg_storage, model.get_as_ws())
    self.runner.storage = self._storage
    flow_converter = FlowConverter(model)
    fsm_def = flow_converter.convert()
    self.runner.create_frfsm(self._cfg.cfg_fsm, fsm_def)
    return

  def reset(self) -> None:
    self.storage.reset()
    self.runner.start()
    return

  def run_all(self, model: FlowModel) -> None:
    self.runner.run_all(model)
    return

  def run_one(self, event: str, idx: int, model: FlowModel) -> None:
    flow_item = model.get_item(idx)
    self.runner.run_step(event, flow_item)
    return
  