import cv2
import os
from .model import Model

class ImagesModel(Model):
  def __init__(self, parent):
    super().__init__()
    self.parent = parent 

    self.path = ''
    self.images_files_list = []

  def get_input_paths(self):

    return self.parent.get_input_paths()


  def get_images_file_names_list(self, path):
    
    self.path = path
    self.images_files_list = [f for f in os.listdir(path) if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.jpeg')]
    
    return self.images_files_list

  def get_selected_file_full_name(self, idx):

    return "{}/{}".format(self.path, self.images_files_list[idx])

  @staticmethod
  def get_image(image_full_file_name):
    cv2image = cv2.imread(image_full_file_name)

    if len(cv2image.shape) > 2:
      b,g,r = cv2.split(cv2image)
      cv2image = cv2.merge((r,g,b))

    return cv2image
