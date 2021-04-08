import os
from .model import Model

class FlowsModel(Model):
  def __init__(self, parent):
    super().__init__()
    self.parent = parent 

    print("FLOWS-MODEL")
    

    self.worksheets_from_all_paths = []
    self.load_worksheets_from_all_paths()

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
    self.worksheets_names = self.read_worksheets_names(path)
    print(self.worksheets_names)
    # flows_meta["flows"] = [{"name": mn, "meta": self.load_worksheet(mn)} for mn in flows_names]

    return


  def load_worksheet(self, worksheets_names):
    # module_meta =  self.parent.factory.get_module_meta(module_names)
    worksheet = {}

    return worksheet



# Getters
  def get_flows_meta(self):
    return self.flows_meta