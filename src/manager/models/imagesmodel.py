import cv2
import os
from .model import Model

class ImagesModel(Model):
  def __init__(self, parent):
    super().__init__()
    self.parent = parent 

    self.path = ''
    self.images_files_list = []
    self.cv2image = None


  def get_images_file_names_list(self, path):
    
    self.path = path
    self.images_files_list = [f for f in os.listdir(path) if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.jpeg')]
    
    return self.images_files_list

  def get_selected_file_full_name(self, idx):

    return "{}/{}".format(self.path, self.images_files_list[idx])

  def get_image(self, image_full_file_name):
    self.cv2image = cv2.imread(image_full_file_name)

    if len(self.cv2image.shape) > 2:
      b,g,r = cv2.split(self.cv2image)
      self.cv2image = cv2.merge((r,g,b))

    return self.cv2image

  def get_original_image_size(self):
    size = (0, 0)
    if self.cv2image is not None:
      size = self.cv2image.shape[:2]
    
    return size