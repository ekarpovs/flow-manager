from typing import List, Dict, Tuple
from flow_model import FlowModel

from .models import *
from .converters import *

class MngrConverter():
  '''
  Fasade for converters 
  '''
  def __init__(self):
    # Create converters
    self._modules_converter = ModuleConverter(self)
    self._flows_converter = FlowConverter()

  @property
  def modules_converter(self):
    return self._modules_converter


  def flowlist_to_flow_names(self, flowmodellist: FlowModelList) ->List[str]:
    return self._flows_converter.flowlist_to_flow_names(flowmodellist)

  def flow_name_to_path_name(self, flow_name) -> Tuple[str, str]:
    return self._flows_converter.flow_name_to_path_name(flow_name)

  def flow_model_to_module_names(self, flow_model: FlowModel):
    return self._flows_converter.flow_model_to_module_names(flow_model)

  def modulelist_to_module_defs(self, modulemodellist: ModuleModelList) ->List[str]:
    return self._modules_converter.modulelist_to_module_defs(modulemodellist)
