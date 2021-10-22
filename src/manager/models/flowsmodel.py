import os
import json
from tkinter.filedialog import asksaveasfilename
import copy

from .model import Model

BEGIN_FLOW_MARKER = {"stm": "glbstm.begin"}
END_FLOW_MARKER = {"stm": "glbstm.end"}

class FlowsModel(Model):
  def __init__(self, parent):
    super().__init__()
    self.parent = parent 

    self.worksheets_from_all_paths = []
    # Current flow
    self.flow_meta = []


# Loaders - model initialization
  def load_worksheets_from_all_paths(self):
    worksheets_paths = self.parent.worksheets_paths
    for path in worksheets_paths:
      self.worksheets_from_all_paths.append(self.load_worksheets(path))
    return  

  def read_worksheets_names(self, path):
    worksheets_names = [f[:-5] for f in os.listdir(path) if f.endswith('.json')]
    return worksheets_names
  
  def load_worksheets(self, path):
    worksheets_names = self.read_worksheets_names(path)
    worksheets = {"path": path, "worksheets": [{"name": wsn,  "content": self.load_worksheet(path, wsn)} for wsn in worksheets_names]}
    return worksheets


  def load_worksheet(self, path, worksheet_name):  
    worksheet = {}
    ffn = "{}/{}.json".format(path, worksheet_name)
    with open(ffn, 'rt') as ws:
      worksheet = json.load(ws)
    worksheet.insert(0, BEGIN_FLOW_MARKER)
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

  # If indent is a non-negative integer, then JSON array elements and object members 
  # will be pretty-printed with that indent level. An indent level of 0, or negative, 
  # will only insert newlines. None (the default) selects the most compact representation.
  def store_flow_meta(self, path, name, meta):
    f = asksaveasfilename(initialfile = '{}.json'.format(name),
      initialdir = path,
      defaultextension=".json",filetypes=[("All Files","*.*"),("Json Documents","*.json")])
    if f is not '':
      with open(f, 'w') as fp:
        if meta[0] == BEGIN_FLOW_MARKER:
          meta.pop(0)
        if meta[-1] == END_FLOW_MARKER:
          meta.pop(-1)
        json.dump(meta, fp, indent=2)
      self.worksheets_from_all_paths = []    
      self.load_worksheets_from_all_paths()
    return


  def add_opearation_to_current_flow(self, oper, oper_params, idx):
    if oper.split('.')[0] == 'glbstm':
      new_oper = {'stm': oper, "params": {}}
      params = new_oper.get('params')
      for p in oper_params:
        # {"type": t, "domain": d, "p_values": pvs, "name": p_name, "value": p_value, "label": l}
        value = p.get('value')
        print(type(value))
        if p.get('type') == 'n':
          value = int(value)
        params[p.get('name')] = value
      # 
    else:
      new_oper = {'exec': oper}
    if len(self.flow_meta) <= 0:
      self.flow_meta.append(BEGIN_FLOW_MARKER)
      self.flow_meta.append(END_FLOW_MARKER)
      idx = 0  
    self.flow_meta.insert(idx, new_oper)
    return self.flow_meta

  def remove_operation_from_current_flow(self, idx):
    if len(self.flow_meta) > 0:
      self.flow_meta.pop(idx)
    return self.flow_meta

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