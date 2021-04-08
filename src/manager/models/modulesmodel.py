import os
import glob

from .model import Model

class ModulesModel(Model):
  def __init__(self, parent):
    super().__init__()
    self.parent = parent 

    print("MODULES-MODEL")

    self.modules_meta = []
    self.load_modules_meta()


  def read_modules_names(self, path):
    names = [f[:-3] for f in os.listdir(path)
                  if f.endswith('.py') and f != '__init__.py' and f != 'tester.py']
    return names

  
  def load_modules_meta(self):
    for mp in self.parent.modules_paths:
      module_meta = {"path": mp, "modules": {}}
      module_names = self.read_modules_names(mp)
      
      module_meta["modules"] = [{"name": mn, "operations": self.load_module_meta(mn)} for mn in module_names]
      # module_meta["modules"] = self.load_module_meta(module_names)
      self.modules_meta.append(module_meta)
        
    print(self.modules_meta)

  
  def load_module_meta(self, module_names):
    module_meta =  self.parent.factory.get_module_meta(module_names)

    return module_meta   
