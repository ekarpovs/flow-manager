# from tkinter import filedialog as fd
import sys
from .models import *
from ..configuration import Configuration

class MngrModel():
  def __init__(self, cfg):

    self.cfg = cfg

    # Create models
    self.modules_model = ModulesModel(self)
    self.flows_model = FlowsModel(self)
    self.images_model = ImagesModel(self)


  def get_modules_paths(self):
    return self.cfg.get_modules_paths()
  
  def get_worksheets_paths(self):
    return self.cfg.get_worksheets_paths()

  def get_input_paths(self):
    return self.cfg.get_input_paths()


  def get_factory(self):
    return self.cfg.get_factory()

