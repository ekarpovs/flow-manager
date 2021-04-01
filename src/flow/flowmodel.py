class FlowModel():
  def __init__(self):
      print("MODEL")

  @classmethod
  def get_modules():

    return []


  def get_module(name):
    
    return [] 


  def get_operation(name):
    
    return 
 
  
  @classmethod
  def get_flow_names():

    return ["compare", "contours", "scanner"]


  def get_flow(self, name):
    # MOCK data
    flows = {
      "compare": 
      {
        "steps":[
          "ws-aux.restore",
          "bsc.fit",
          "cmp.cmp_mse",
          "cmp.cmp_ssim",
          "cmp.cmp_psnr",
          "cmp.cmp_norm"
        ]
      },
      "contours":
      {
        "steps":[
          "clrs.bgrto",
          "cntrs.find",
          "cntrs.sort",
          "draw.contours"
        ]
      },
      "scanner":
      {
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
  