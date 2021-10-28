from typing import List, Dict, Tuple

from src.manager.models.flow.currentflowmodel import CurrentFlowModel



class FlowConverter():
  '''
  Maps data from flow model to flow view and versa
  '''
  def __init__(self):
    pass

  @staticmethod
  def split_ws_name(ws_name) -> Tuple[str, str]:
    name, path = ws_name.split('<')
    name = name[:-1]
    path =  path[:-1]
    return (path, name)
    