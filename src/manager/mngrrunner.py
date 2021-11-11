from typing import Dict, List

from flow_model import FlowModel
from flow_runner import Runner
from flow_converter import FlowConverter
from flow_storage import FlowStorage

from ..configuration import Configuration

class MngrRunner():
  '''
  Flow runner client
  '''
  
  def __init__(self, cfg: Configuration) -> None:
    self._cfg = cfg
    self._runner = Runner()
    self._stotage = None
    self._model = None
    return

  @property
  def runner(self):
    return self._runner

  @property
  def storage(self):
    return self._stotage

  @property
  def initialized(self) -> bool:
    return self.runner.initialized


  def build(self, model: FlowModel) -> None:
    self._model = model
    self._stotage = FlowStorage(self._cfg.cfg_storage, model.worksheet)
    self.runner.storage = self._stotage
    flow_converter = FlowConverter(model)
    fsm_def = flow_converter.convert()
    self.runner.create_frfsm(self._cfg.cfg_fsm, fsm_def)
    return

  def reset(self) -> None:
    self.storage.reset()
    self.runner.start()
    return

  def run_all(self) -> None:
    self.runner.run_all(self._model)
    return

  def run_one(self, event: str, idx: int) -> None:
    flow_item = self._model.get_item(idx)
    self.runner.run_step(event, flow_item)
    return
  
  @property
  def state_idx(self):
    return self.runner.state_idx