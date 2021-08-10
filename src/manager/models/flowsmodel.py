import os
import json
import copy

from .model import Model

END_FLOW_MARKER = {"stm": "glbstm.end"}

class FlowsModel(Model):
  def __init__(self, parent):
    super().__init__()
    self.parent = parent 
  

    self.worksheets_from_all_paths = []

    # Current flow
    self.flow_meta = []


# Loaders - model initialization
  def read_worksheets_names(self, path):
    worksheets_names = [f[:-5] for f in os.listdir(path) if f.endswith('.json')]

    return worksheets_names
  
  def load_worksheets_from_all_paths(self):
    worksheets_paths = self.parent.get_worksheets_paths()
    for path in worksheets_paths:
      self.worksheets_from_all_paths.append(self.load_worksheets(path))
       

  def load_worksheets(self, path):
    worksheets_names = self.read_worksheets_names(path)
    worksheets = {"path": path, "worksheets": [{"name": wsn,  "content": self.load_worksheet(path, wsn)} for wsn in worksheets_names]}

    return worksheets


  def load_worksheet(self, path, worksheets_names):  
    worksheet = {}
    ffn = "{}/{}.json".format(path, worksheets_names)
    with open(ffn, 'rt') as ws:
      worksheet = json.load(ws)
    worksheet.append(END_FLOW_MARKER)
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

  def load_flow_meta(self, path, name):
    if path != "":
      ws = self.get_worksheet(path, name)
      self.flow_meta = copy.deepcopy(ws)
    else:
      self.flow_meta = []

    return self.flow_meta

  def add_opearation_to_current_flow(self, oper, idx):
    new_oper = {'exec': oper}
    if len(self.flow_meta) <= 0:
      idx = 0  
    self.flow_meta.insert(idx, new_oper)

    return self.flow_meta


  def remove_operation_from_current_flow(self, idx):
    self.flow_meta.pop(idx)

    return self.flow_meta

  def save_current_flow_meta(self, path, name, meta):
    print("path", path)
    print("name", name)
    print("meta", meta)
    pass


  def update_current_flow_params(self, operation_params_item):
    idx = operation_params_item['idx']
    flow_item_to_update = self.flow_meta[idx]
    if 'params' not in flow_item_to_update:
      flow_item_to_update['params'] = {}
    # print("before", flow_item_to_update)
    for param in operation_params_item['params']:
      # print(param['name'])
      pn = param['name'].strip() 
      pv = param['value'] 
      flow_item_to_update['params'][pn] = pv

    # print("after", flow_item_to_update)
      
    return flow_item_to_update