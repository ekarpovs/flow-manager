from tkinter.constants import S
from .converter import Converter

class FlowsConverter(Converter):
  def __init__(self, parent):
    super().__init__()
    self.parent = parent 

    print("FLOWS-CONVERTER")


  @staticmethod
  def convert_worksheets_names(worksheets_names):
    names = []
    worksheets_names = [{'name': 'new', 'path': ''}, *worksheets_names]
    for wsn in worksheets_names:
      name = "{} <{}>".format(wsn['name'], wsn['path'])
      names.append(name)

    return names


  @staticmethod
  def convert_ws_item(item):
    name, path = item.split('<')
    name = name[:-1]
    path =  path[:-1]

    return path, name
    

  @staticmethod
  def convert_flow_meta(flow_meta):
    names = []
    if 'steps' in flow_meta:
      steps = flow_meta['steps']
      for step in steps:
        names.append(step['exec'])

    return names