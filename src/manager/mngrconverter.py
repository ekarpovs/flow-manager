from typing import List, Tuple

from .models import *
from .converters import *

class MngrConverter():
  '''
  Fasade for converters 
  '''
  def __init__(self):
    # Create converters
    self._module = ModuleConverter()
    self._flow = FlowConverter()

  @property
  def module(self) -> ModuleConverter:
    return self._module

  @property
  def flow(self) -> FlowConverter:
    return self._flow

  def split_ws_name(self, ws_name) -> Tuple[str, str]:
    return self.flow.split_ws_name(ws_name)

  def modulelist_to_module_defs(self, modulemodellist: ModuleModelList) ->List[str]:
    return self.module.modulelist_to_module_defs(modulemodellist)
