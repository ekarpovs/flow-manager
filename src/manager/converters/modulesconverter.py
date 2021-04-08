from .converter import Converter

class ModulesConverter(Converter):
  def __init__(self, parent):
    super().__init__()
    self.parent = parent 

    print("MODULES-CONVERTER")
