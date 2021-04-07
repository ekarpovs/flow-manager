import sys
import json 

class FlowRunner():
  def __init__(self):

    print("RUNNER")

    # TODO: via configuration
    factory_path = "../operation-loader"
    modules_paths = ["../modules-and-worksheets/modules", "../modules-and-worksheets/modules-common"]
    # set paths to external modules located outside the package
    for path in modules_paths:
      sys.path.append(path)

    # import factory fo loading modules outside of the package.
    # temporary since the factory is not installed via pip
    sys.path.append(factory_path)
    from factory import get
    self.get = get
