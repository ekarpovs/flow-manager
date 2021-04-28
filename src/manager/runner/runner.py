from tkinter.constants import E
from .context import Context
from .contextstack import ContextStack
from .wrapper import flowoperation

class Runner():
  def __init__(self, cfg):

    self.contextstack = ContextStack()
    self.get = cfg.get_factory().get
    self.cv2image = None
    self.counter = 0
 
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

  def init_step(self):
    if self.contextstack.isEmpty():
      self.counter = 0
      kwargs = {}
      kwargs['orig'] = self.cv2image
      kwargs['image'] = self.cv2image
    else:
      kwargs = self.contextstack.peek().kwargs_after

    return kwargs

  def increment_counter(self):
    self.counter += 1
    return

  def dencrement_counter(self):
    self.counter -= 1
    return


  def run(self, flow_meta, one = False):
    steps = flow_meta['steps']
    image = None

    execute = True
    while(execute and self.counter < len(steps)):
      
      current_step = steps[self.counter]
      self.increment_counter()

      image = self.run_step(current_step)

      if one == True: 
        execute = False

    return image




  def run_step(self, current_step):
    kwargs = self.init_step()
    # Craete the step context with input values 
    step_context = Context(**kwargs)
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
    if self.contextstack.isEmpty() or self.counter == 0:
      print("On the top")
      return None

    kwargs = self.contextstack.peek().kwargs_before
    self.contextstack.pop()
    self.dencrement_counter()
    
    return kwargs['image']  


  def top(self):
    self.contextstack.reset()
    self.counter = 0
    return
