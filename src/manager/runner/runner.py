import cv2
from .context import Context
from .contextstack import ContextStack

class Runner():
  def __init__(self, cfg):

    print("RUNNER")
    self.contextstack = ContextStack()
    self.cfg = cfg
    self.get = cfg.get_factory().get
    self.cv2image = None
  

  def load_image(self):
    # TODO: get from view
    image_full_file_name = "{}\scan-01.jpg".format(self.cfg.get_input_path())
    self.cv2image = cv2.imread(image_full_file_name)

    if len(self.cv2image.shape) > 2:
      b,g,r = cv2.split(self.cv2image)
      self.cv2image = cv2.merge((r,g,b))

    return self.cv2image


  def run_flow(self, flow_meta):
    kwargs = {}
    kwargs['orig'] = self.cv2image
    kwargs['image'] = self.cv2image
    steps = flow_meta['steps']
    for step in steps:
      # load the step's function
      operation = self.get(step['exec'])
      kwargs = operation(step, **kwargs)    

    return kwargs['image']



  def step_back(self):
    if self.contextstack.isEmpty():
      print("On the top")
      return None

    kwargs = self.contextstack.peek().kwargs
    step_context = self.contextstack.pop()
    print(step_context.step_meta)
    
    return kwargs['image']  



  def run_step(self, flow_meta):
    if self.contextstack.isEmpty():
      kwargs = {}
      kwargs['orig'] = self.cv2image
      kwargs['image'] = self.cv2image
    else:
      kwargs = self.contextstack.peek().kwargs

    steps = flow_meta['steps']
    if self.contextstack.size() >= len(steps):
      print("No more steps")
      return None

    current_step = steps[self.contextstack.size()]
    # load the step's function
    operation = self.get(current_step['exec'])
    kwargs = operation(current_step, **kwargs)    
    # Store the step context with result
    step_context = Context(current_step, **kwargs)
    self.contextstack.push(step_context)

    return kwargs['image']
