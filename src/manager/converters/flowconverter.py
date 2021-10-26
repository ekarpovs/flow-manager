from typing import List, Dict, Tuple

from flow_model import FlowModel, FlowItemModel, FlowItemType

from ..models import FlowModelList


class FlowConverter():
  '''
  Maps data from flow model to flow view and versa
  '''
  def __init__(self):
    pass

  @staticmethod
  def flowlist_to_flow_names(flowlist: FlowModelList) ->List[str]:
    names = []
    names.append(f'new <>')
    for flow in flowlist:
      name = flow.name
      path = flow.path
      name = f'{name} <{path}>'
      names.append(name)
    return names


  @staticmethod
  def flow_name_to_path_name(flow_name) -> Tuple[str, str]:
    name, path = flow_name.split('<')
    name = name[:-1]
    path =  path[:-1]
    return (path, name)
    

  @staticmethod
  def flow_model_to_module_names(flow_model: FlowModel):
    names = []
    for item in flow_model.items:
      names.append(item.name)
    return names
