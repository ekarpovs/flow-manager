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


  def load_modules_meta(self):
      for mp in self.parent.modules_paths:
        module_meta = {"path": mp, "modules": {}}
        pattern = "{}/*.py".format(mp)
        md_names = [
          md 
          for md in [md[len(md)-1].split('.')[0] 
          for md in [md.replace('\\', '/').split('/') 
          for md in [mds for mds in glob.glob(pattern)]]] if not md.startswith('__')
        ]
        
        
        module_meta["modules"] = md_names
        self.modules_meta.append(module_meta)
        
      print(self.modules_meta)

