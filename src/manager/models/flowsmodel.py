from .model import Model

class FlowsModel(Model):
  def __init__(self, parent):
    super().__init__()
    self.parent = parent 

    print("FLOWS-MODEL")
