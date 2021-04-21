import os
import json
from .model import Model

class ImagesModel(Model):
  def __init__(self, parent):
    super().__init__()
    self.parent = parent 





  def get_input_paths(self):

    return self.parent.get_input_paths()


  def load_images_files_list(self, path):
    images_files = []
    
    return images_files