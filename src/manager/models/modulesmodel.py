import os
import json

import operation_loader

from .model import Model

class ModulesModel(Model):
  def __init__(self, parent):
    super().__init__()
    self.parent = parent 

    self.modules_meta_from_all_paths = []

# Metadata
# Loaders - model initialization
  def read_modules_names(self, path):
    names = [f[:-3] for f in os.listdir(path)
                  if f.endswith('.py') and f != '__init__.py' and f != 'tester.py']
    return names

  
  def load_modules_meta_from_all_paths(self):
    modules_paths = self.parent.get_modules_paths()
    for path in modules_paths:
      self.modules_meta_from_all_paths.append(self.load_modules_meta(path))
       

  def load_modules_meta(self, path):
    modules_meta = {"path": path, "modules": {}}
    modules_names = self.read_modules_names(path)     
    modules_meta["modules"] = [{"name": mn, "meta": self.load_module_meta(mn)} for mn in modules_names]

    return modules_meta


  def load_module_meta(self, module_name):
    module_meta = operation_loader.get_module_meta(module_name)

    module_meta = self.format_module_meta(module_meta)
    self.store_module_meta(module_name, module_meta)

    return module_meta   

  @staticmethod
  def format_module_meta(module_meta):
    module_meta['descr'] = module_meta['descr'].replace('\n', '') 
    meta = module_meta['meta']
    for fmeta in meta:
      fdoc = fmeta['doc']
      fdoc = fdoc.strip().split('\n')
      fd = []
      for line in fdoc:
        line = line.expandtabs().strip()
        if line != "":
          fd.append(line)
      fmeta['doc'] = fd
    
    return module_meta
    

  @staticmethod
  def store_module_meta(module_name, module_meta):
    # temporary
    path = "../data/meta"
    ffn = "{}/{}.json".format(path, module_name)
    with open(ffn, "w") as outfile: 
      json.dump(module_meta, outfile, indent = 4, sort_keys = True)


# Operation documentation
  @staticmethod
  def read_operation_doc(module_name, oper_name):
    path = "../data/meta"
    ffn = "{}/{}.json".format(path, module_name)
    with open(ffn, 'rt') as f:
      meta = json.load(f)['meta']

    for fmeta in meta:
      fname = fmeta['name']
      if fname == oper_name:
        fdoc = fmeta['doc']

        return fdoc
    
    return ''

  @staticmethod
  def read_operation_params_defenition(module_name, oper_name):
    fdoc = ModulesModel.read_operation_doc(module_name, oper_name)
    
    fpdef = []
    for line in fdoc:
      if line.startswith('--'):
        fpdef.append(line)
    
    return fpdef


# Getters
  def get_modules_meta(self):
    return self.modules_meta_from_all_paths
