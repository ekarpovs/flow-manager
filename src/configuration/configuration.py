import sys
import json

class Configuration():
  def __init__(self):
    self.load_configuration()


  def load_configuration(self):
    # TODO read from config.json
    self.factory_path = "../operation-loader"

    self.input_path="d:/Projects/mine/github/work-shop/data/input" 
    self.result_path="d:/Projects/mine/github/work-shop/data/output" 
    self.modules_paths = ["../modules-and-worksheets/modules", "../modules-and-worksheets/modules-common"]
    self.worksheets_paths=["d:/Projects/mine/github/work-shop/modules_and_worksheets/worksheets"]


  def get_factory_path(self):
    return self.input_path


  def get_input_path(self):
    return self.input_path

  def get_result_path(self):
    return self.result_path

  def get_modules_paths(self):
    return self.modules_paths

  def get_worksheets_paths(self):
    return self.worksheets_paths

