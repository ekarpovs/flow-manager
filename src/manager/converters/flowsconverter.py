from .converter import Converter

class FlowsConverter(Converter):
  def __init__(self, parent):
    super().__init__()
    self.parent = parent 

    print("FLOWS-CONVERTER")
