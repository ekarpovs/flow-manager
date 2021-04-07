from . import Model

class ModulesModel(Model):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 

    print("MODULES-MODEL")
