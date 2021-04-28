from tkinter.constants import E
from .context import Context
from .contextstack import ContextStack
from .wrapper import flowoperation

class Runner():
  def __init__(self, cfg):

    self.contextstack = ContextStack()
    self.get = cfg.get_factory().get
    self.cv2image = None
  
  def set_input_image(self, cv2image):
    self.cv2image = cv2image

    return

  def preprocessor(self, step, operation):

    gforinrange = step.get('gforinrange', None)
    if gforinrange is not None:
      param = step['gforinrange'].get('i', "")
      x = step['gforinrange'].get('x', 0)
      y = step['gforinrange'].get('y', 10)
      s = step['gforinrange'].get('s', 1)
      d = step['gforinrange'].get('d', 0)
      print("perprocessor - gforinrange: param, x, y, s, d", param, x, y, s, d)

    return operation

  def init_step_input(self):
    if self.contextstack.isEmpty():
      kwargs = {}
      kwargs['orig'] = self.cv2image
      kwargs['image'] = self.cv2image
    else:
      kwargs = self.contextstack.peek().kwargs_after

    return kwargs


  def run(self, flow_meta, one = False):
    steps = flow_meta['steps']

    # for idx, step in enumerate(steps):
    execute = True
    idx = 0
    while(execute and idx < len(steps)):
      if self.contextstack.size() >= len(steps):
        print("No more steps")
        return None

      # current_step = steps[self.contextstack.size()]
      current_step = steps[self.contextstack.size()]

      image = self.run_step(current_step)
      idx += 1
      if one == True: 
        execute = False

    return image




  def run_step(self, current_step):
    kwargs = self.init_step_input()
    # Craete the step context with input values 
    step_context = Context(0, current_step, **kwargs)
    # load the step's function
    operation = self.get(current_step['exec'])
    wrapped = flowoperation(operation)
    # Run the step
    kwargs = wrapped(current_step, **kwargs)    
    # Set result to step context
    step_context.set_after(**kwargs)
    # Store the context
    self.contextstack.push(step_context)

    return kwargs['image']


  def back(self):
    if self.contextstack.isEmpty():
      print("On the top")
      return None

    kwargs = self.contextstack.peek().kwargs_before
    step_context = self.contextstack.pop()
    
    return kwargs['image']  

  def top(self):
    self.contextstack.reset()
    return
