from tkinter.constants import S
from .converter import Converter

class FlowsConverter(Converter):
  def __init__(self, parent):
    super().__init__()
    self.parent = parent 

    print("FLOWS-CONVERTER")


  @staticmethod
  def split_ws_item(item):
    name, path = item.split('<')
    name = name[:-1]
    path =  path[:-1]

    return path, name
    
  @staticmethod
  def get_empty_flow():
    return {'steps':[]}
