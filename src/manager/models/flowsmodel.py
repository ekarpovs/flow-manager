import os
import json
from tkinter.constants import W
from .model import Model

class FlowsModel(Model):
  def __init__(self, parent):
    super().__init__()
    self.parent = parent 

    print("FLOWS-MODEL")
    

    self.worksheets_from_all_paths = []

    # Current flow
    self.flow_meta = {}


# Loaders - model initialization
  def read_worksheets_names(self, path):
    worksheets_names = [f[:-5] for f in os.listdir(path) if f.endswith('.json')]

    return worksheets_names
  
  def load_worksheets_from_all_paths(self):
    for path in self.parent.worksheets_paths:
      self.worksheets_from_all_paths.append(self.load_worksheets(path))
       

  def load_worksheets(self, path):
    # worksheets = {"path": path, "flows": {}}
    worksheets_names = self.read_worksheets_names(path)
    worksheets = {"path": path, "worksheets": [{"name": wsn,  "content": self.load_worksheet(path, wsn)} for wsn in worksheets_names]}

    return worksheets


  def load_worksheet(self, path, worksheets_names):  
    worksheet = {}
    ffn = "{}/{}.json".format(path, worksheets_names)
    with open(ffn, 'rt') as ws:
      worksheet = json.load(ws)

    return worksheet



# Getters
# for all paths
  def get_worksheets_from_all_paths(self):
    wss_all = self.worksheets_from_all_paths
    return [wss['worksheets'] for wss in wss_all]

  def get_worksheets_names_from_all_paths(self):
    worksheets_names = []
    for set in self.worksheets_from_all_paths:
      path = set['path']
      for wss in set['worksheets']:
        worksheets_names.append({"name":wss['name'], "path": path})    

    return worksheets_names

# by path
  def get_worksheets(self, path):
    wss_all = self.worksheets_from_all_paths
    return [wss['worksheets'] for wss in wss_all if wss['path'] == path][0]
  
  def get_worksheets_names(self, path):
    return [ws['name'] for ws in self.get_worksheets(path)]


  def get_worksheet(self, path, name):
    return [ws['content'] for ws in self.get_worksheets(path) if ws['name'] == name][0]

  def get_flow_meta(self, path, name):
    self.flow_meta = self.get_worksheet(path, name)

    return self.flow_meta
