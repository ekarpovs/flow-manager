import os

from .model import Model

class ModulesModel(Model):
  def __init__(self, parent):
    super().__init__()
    self.parent = parent 

    print("MODULES-MODEL")

    self.modules_meta_from_all_paths = []

# Loaders - model initialization
  def read_modules_names(self, path):
    names = [f[:-3] for f in os.listdir(path)
                  if f.endswith('.py') and f != '__init__.py' and f != 'tester.py']
    return names

  
  def load_modules_meta_from_all_paths(self):
    for path in self.parent.modules_paths:
      self.modules_meta_from_all_paths.append(self.load_modules_meta(path))
       

  def load_modules_meta(self, path):
    modules_meta = {"path": path, "modules": {}}
    modules_names = self.read_modules_names(path)     
    modules_meta["modules"] = [{"name": mn, "meta": self.load_module_meta(mn)} for mn in modules_names]

    return modules_meta


  def load_module_meta(self, module_names):
    module_meta =  self.parent.factory.get_module_meta(module_names)

    return module_meta   

# Getters
  def get_modules_meta(self):
    return self.modules_meta_from_all_paths