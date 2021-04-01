class FlowModel():
  def __init__(self):
      print("MODEL")


  def get_modules(self):
    # modules = {
    #   "name": "blur",
    #   "descr": "Bluring operations",
    #   "opers": {
    #       {
    #         "name": "avg",
    #         "descr": "Performs average bluring."
    #       },
    #       {
    #         "name": "gaus",
    #         "descr": "Performs Gausian bluring."
    #       }
    #   },
    #   "name": "bsc",
    #   "descr": "Basic operations",
    #   "opers": {
    #     {
    #       "name": "crop",
    #       "descr": "Crops an image."
    #     },
    #     {
    #       "name": "flip",
    #       "descr": "Flips an image."
    #     }
    #   },
    #   "name": "cnts",
    #   "descr": "Contours operations",
    #   "opers": {
    #     {
    #       "name": "find",
    #       "descr": "Finds contours of an image."
    #     },
    #     {
    #       "name": "sort",
    #       "descr": "Sorts contours."
    #     }
    #   }
    # }

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


  def get_module(name):
    
    return [] 


  def get_operation(name):
    
    return 
 
  
  def get_flow_names(self):

    return ["compare", "contours", "scanner"]


  def get_flow(self, name):
    # MOCK data
    flows = {
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

    flow  = flows[name]

    return flow['steps']
    # return ["clr.bgrto", "blur.gaus", "edge.canny", "cntrs.find",
    #   "cntrs.sort", "draw.contours", "cntrs.sel_rect", "bsc.transform"]


  def set_operation():
    
    return 


  def remove_operation():

    return  
  