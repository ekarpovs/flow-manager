class State:
  class Statement:
    def __init__(self, parent):
      self.parent = parent
      self.type = None
      self.param = {}
      self.counter = 0
      self.begin = 0
      self.end = 0

    def set(self, step):
      self.counter = self.parent.counter
      gforinrange = step.get('gforinrange', None)
      if gforinrange is not None:
        self.type = 'gforinrange'
        self.param['x'] = step['gforinrange'].get('x', 0)
        self.param['y'] = step['gforinrange'].get('y', 10)
        self.param['s'] = step['gforinrange'].get('s', 1)
        self.param['d'] = step['gforinrange'].get('d', 0)
        self.param['i'] = step['gforinrange'].get('i', '')

        self.begin = self.counter
        self.end = self.begin + self.param['d']

      return

    def get_counter(self):
      self.counter += 1
      if self.type and (self.counter >= self.end):
        self.counter = self.begin

      return self.counter


  def __init__(self):
    self.reset()


  def reset(self):
    self.counter = -1
    self.steps = None
    self.statement = self.Statement(self)

    return    

  def ready(self):
    return self.counter > -1


  def set(self, steps):
    self.steps = steps
    self.counter = 0

    return


  def next(self):
    step = None
    if self.counter < len(self.steps):
      step = self.steps[self.counter]
      self.statement.set(step)      
      self.counter = self.statement.get_counter()

    return step


  def prev(self):
    step = None
    if self.counter > 0:
      self.counter -= 1
      step = self.steps[self.counter]

    return step

  