class FlowModel():
  def __init__(self):
      print("MODEL")


# Meta data
  def get_modules_meta(self):
    modules = {
      "blur": {
      "descr": "Bluring operations",
      "opers": [
          {
            "name": "avg",
            "descr": "Performs average bluring."
          },
          {
            "name": "gaus",
            "descr": "Performs Gausian bluring."
          }
        ]
      },
      "bsc": {
      "descr": "Basic operations",
      "opers": [
          {
            "name": "crop",
            "descr": "Crops an image."
          },
          {
            "name": "flip",
            "descr": "Flips an image."
          }
        ]
      },
      "cntrs": {
      "descr": "Contours operations",
      "opers": [
          {
            "name": "find",
            "descr": "Finds contours of an image."
          },
          {
            "name": "sort",
            "descr": "Sorts contours."
          }
        ]
      }
    }

    return modules

  
  def get_work_sheet_names(self):

    return ["compare", "contours", "scanner"]


  def get_work_sheet(self, work_sheet_name):
    # MOCK data
    work_sheets = {
      "compare": {
        "steps":[
          "ws-aux.restore",
          "bsc.fit",
          "cmp.cmp_mse",
          "cmp.cmp_ssim",
          "cmp.cmp_psnr",
          "cmp.cmp_norm"
        ]
      },
      "contours": {
        "steps":[
          "clrs.bgrto",
          "cntrs.find",
          "cntrs.sort",
          "draw.contours"
        ]
      },
      "scanner": {
        "steps":[
          "clrs.bgrto",
          "blur.gaus",
          "edge.canny",
          "cntrs.find",
          "cntrs.sort",
          "draw.contours",
          "cntrs.sel_rect",
          "bsc.transform"
        ]
      }                
    }

    work_sheet  = work_sheets[work_sheet_name]
    return work_sheet


# Real objects

  def set_operation():
    
    return 


  def remove_operation():

    return  
  
  def get_module(name):
    
    return [] 


  def get_operation(name):
    
    return 
