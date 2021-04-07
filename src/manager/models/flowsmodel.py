from . import Model

class FlowsModel(Model):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 

    print("FLOWS-MODEL")
