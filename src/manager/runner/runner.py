from tkinter.constants import E
from .state import State
from .context import Context
from .contextstack import ContextStack
from .wrapper import flowoperation

class Runner():
  def __init__(self, cfg):
    self.state = State()
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


  def init_step(self):
    if self.contextstack.isEmpty():
      # self.state.reset()
      kwargs = {}
      kwargs['orig'] = self.cv2image
      kwargs['image'] = self.cv2image
    else:
      kwargs = self.contextstack.peek().kwargs_after

    return kwargs


  def run(self, flow_meta, one = False):
    if not one: 
      self.state.reset()
      self.contextstack.reset()

    steps = flow_meta['steps']
    if not self.state.ready():
      self.state.set(steps)

    image = None

    execute = True
    while(execute):
      current_step = self.state.next()
      if current_step is not None:
        image = self.run_step(current_step)
        if one == True: 
          execute = False
      else:
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

    image = None
    if not self.state.prev():
      self.state.reset()
      self.contextstack.reset()
      print("On the top")
      return None
    else:
      image = self.contextstack.peek().kwargs_before['image']
      self.contextstack.pop()
    
    return image


  def top(self):
    self.state.reset()
    self.contextstack.reset()

    return
