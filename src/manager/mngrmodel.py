# from tkinter import filedialog as fd
import sys
from .models import *
from ..configuration import Configuration

class MngrModel():
  def __init__(self):
    print("MNGR-MODEL")

    cfg = Configuration()
    self.modules_paths = cfg.get_modules_paths()
    self.worksheets_paths = cfg.get_worksheets_paths()
    self.input_path = cfg.get_input_path()
    self.result_path = cfg.get_result_path()

    self.factory = self.import_factory_ref(cfg)

    # Create models
    self.modules_model = ModulesModel(self)
    self.flows_model = FlowsModel(self)


  @staticmethod
  def import_factory_ref(cfg):  
    # import factory fo loading modules from outside of the package.
    # temporary, since the factory is not installed via pip
    factory_path = cfg.get_factory_path()
    sys.path.append(factory_path)
    import factory

    return factory

# Getters


# Getters wrappers






# Meta data

  # # def get_work_sheet_names_mock(self):
  # #   # TODO: from FS 
  # #   names = ["compare", "contours", "scanner"]
    
  # #   # add the 'new' option
  # #   return ["new", *names]

  
  # def read_work_sheet_names(self):

  #   # Read from ws folder
  #   self.work_sheet_names = ["compare", "contours", "scanner"]

  #   return

  # def load_work_sheet(self, work_sheet_name):
  #   # Read from ws folder
    

  #   self.work_sheet = self.add_default_steps(work_sheet_name)

  #   return


  
  # def get_work_sheet_names(self):
    
  #   return ["new", *self.work_sheet_names]


  # def get_work_sheet(self):

  #   return self.work_sheet




  # # def get_work_sheet_mock(self, work_sheet_name):
  # #   # MOCK data
  # #   work_sheets = {
  # #     "compare": {
  # #       "steps":[
  # #         "bsc.fit",
  # #         "cmp.cmp_mse",
  # #         "cmp.cmp_ssim",
  # #         "cmp.cmp_psnr",
  # #         "cmp.cmp_norm"
  # #       ]
  # #     },
  # #     "contours": {
  # #       "steps":[
  # #         "clrs.bgrto",
  # #         "cntrs.find",
  # #         "cntrs.sort",
  # #         "draw.contours"
  # #       ]
  # #     },
  # #     "scanner": {
  # #       "steps":[
  # #         "clrs.bgrto",
  # #         "blur.gaus",
  # #         "edge.canny",
  # #         "cntrs.find",
  # #         "cntrs.sort",
  # #         "draw.contours",
  # #         "cntrs.sel_rect",
  # #         "bsc.transform"
  # #       ]
  # #     }                
  # #   }

  # #   work_sheet  = work_sheets[work_sheet_name]
  # #   work_sheet = self.add_default_steps(work_sheet)

  # #   return work_sheet

  # def add_default_steps(self, work_sheet):
  #   # The first step will always "start" for get the flow input
  #   ffn = "{}/{}".format(self.input_path, self.image_file_name)
  #   first_step = [{"exec": "common.start", "ffn": ffn}]

  #   # The last step will always - store to store the flow output
  #   ffn = "{}/result-{}".format(self.result_path, self.image_file_name)
  #   last_step = [{"exec": "common.store", "ffn": ffn}]

  #   steps = [*first_step, *work_sheet, *last_step]

  #   return work_sheet


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
