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
    self._stotage = None
    return

  @property
  def runner(self) -> Runner:
    return self._runner

  @property
  def storage(self) -> FlowStorage:
    return self._stotage

  @property
  def initialized(self) -> bool:
    return self.runner.initialized

  @property
  def state_idx(self) -> int:
    return self.runner.state_idx

  def get_current_output(self) -> Tuple[List[Tuple[str, FlowDataType]], Dict]:
    state_id = self.runner.output_from_state
    data = self.storage.get_state_output_data(state_id)
    refs = self.storage.get_state_output_refs(state_id)
    t_refs = [(ref.ext_ref, ref.int_ref,ref.data_type) for ref in refs]  
    return (t_refs, data)
  

  def build(self, model: FlowModel) -> None:
    self._stotage = FlowStorage(self._cfg.cfg_storage, model.get_as_ws())
    self.runner.storage = self._stotage
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
  