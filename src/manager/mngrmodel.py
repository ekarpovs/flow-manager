# from tkinter import filedialog as fd
import sys
from .models import *
from ..configuration import Configuration

class MngrModel():
  def __init__(self):
    print("MNGR-MODEL")

    self.cfg = Configuration()

    # Create models
    self.modules_model = ModulesModel(self)
    self.flows_model = FlowsModel(self)


  def get_modules_paths(self):
    return self.cfg.get_modules_paths()
  
  def get_worksheets_paths(self):
    return self.cfg.get_worksheets_paths()

  def get_factory(self):
    return self.cfg.get_factory()



  # def load_image(self):
  #   title="Load Image for Processing"
  #   file_types = (
  #     ('image files', '*.jpg, *.jpeg, *.png'),
  #     ('All files', '*.*')
  #   )
  #   self.image_file_name = fd.askopenfilename(title=title, initialdir=self.input_path, filetypes=file_types)

  #   self.cv2image = cv2.imread(self.image_file_name)
  #   if len(self.cv2image.shape) > 2:
  #     b,g,r = cv2.split(self.cv2image)
  #     self.cv2image = cv2.merge((r,g,b))

  #   return self.cv2image


  # def get_image_orig(self):
  #   return self.cv2image

