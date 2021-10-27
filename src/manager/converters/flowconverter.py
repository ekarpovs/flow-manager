from typing import List, Dict, Tuple

from src.manager.models.activeflow.activeflowmodel import ActiveFlowModel



class FlowConverter():
  '''
  Maps data from flow model to flow view and versa
  '''
  def __init__(self):
    pass

  # @staticmethod
  # def flowlist_to_flow_names(flowlist: FlowModelList) ->List[str]:
  #   names = []
  #   names.append(f'new <>')
  #   for flow in flowlist.flowmodellist:
  #     name = flow.name
  #     path = flow.path
  #     name = f'{name} <{path}>'
  #     names.append(name)
  #   return names

  @staticmethod
  def split_ws_name(ws_name) -> Tuple[str, str]:
    name, path = ws_name.split('<')
    name = name[:-1]
    path =  path[:-1]
    return (path, name)
    
  @staticmethod
  def flow_model_to_module_names(flow_model: ActiveFlowModel):
    names = []
    for item in flow_model.item.items:
      name = item.name 
    names.append(name)
    return names
