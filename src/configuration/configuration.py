import sys
import json

class Configuration():
  def __init__(self):
    self.load_configuration()


  # Loaders
  def load_configuration(self):
    # TODO read from config.json
    self.factory_path = "../operation-loader"

    self.input_paths=["../data/input"]
    self.result_path="../data/output" 
    self.modules_paths = ["../modules-and-worksheets/modules", "../modules-and-worksheets/modules-common"]
    self.worksheets_paths=["../modules-and-worksheets/worksheets", "../modules-and-worksheets/worksheets-ocv"]

    # Set paths for access factory and modules outside of the application
    for path in self.modules_paths:
      sys.path.append(path)
    # Till the operation-loader is not installed via pip
    sys.path.append(self.factory_path)
    import factory
    self.factory = factory
  

  def get_factory(self):
    return self.factory

  def get_input_paths(self):
    return self.input_paths

  def get_result_path(self):
    return self.result_path

  def get_modules_paths(self):
    return self.modules_paths

  def get_worksheets_paths(self):
    return self.worksheets_paths
