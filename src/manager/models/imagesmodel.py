import os
import json
from .model import Model

class ImagesModel(Model):
  def __init__(self, parent):
    super().__init__()
    self.parent = parent 





  def get_input_paths(self):

    return self.parent.get_input_paths()


  def get_images_file_names_list(self, path):
    images_files_list = [f for f in os.listdir(path) if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.jpeg')]
    
    return images_files_list

