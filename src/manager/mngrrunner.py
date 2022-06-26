from flow_model import FlowModel
from flow_runner import Runner
from flow_storage import FlowStorage

from ..configuration import Configuration

class MngrRunner():
  '''
  Flow runner client
  '''
  
  def __init__(self, cfg: Configuration) -> None:
    self._cfg = cfg
    self._runner = Runner()
    return

  @property
  def storage(self) -> FlowStorage:
    return self._runner.storage

  @property
  def initialized(self) -> bool:
    return self._runner.initialized

  @property
  def state_idx(self) -> int:
    return self._runner.state_idx

  @property
  def state_id(self) -> str:
    return self._runner.state_id

  @property
  def output_from_state(self) -> str:
    return self._runner._output_from_state

  def build(self, model: FlowModel) -> None:
    self._runner.build(self._cfg.cfg_fsm, model)
    return

  def reset(self) -> None:
    self._runner.reset()
    return

  def run_all(self) -> None:
    self._runner.run_all()
    return

  def run_one(self, event: str, idx: int) -> None:
    self._runner.run_step(event, idx)
    return
  