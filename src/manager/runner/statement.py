class Statement():
  def __init__(self, parent):
    self.parent = parent
    self.type = None
    self.param = {}
    self.counter = 0
    self.begin = 0
    self.end = 0

  def set(self, step):
    self.counter = self.parent.counter
    if self.type is not None:
      return

    self.step = step
    gforinrange = step.get('gforinrange', None)
    if gforinrange is not None:
      self.gforinrange_set(step)

    return


  def gforinrange_set(self, step):
    self.type = 'gforinrange'
    self.param['x'] = step['gforinrange'].get('x', 0)
    self.param['y'] = step['gforinrange'].get('y', 10)
    self.param['s'] = step['gforinrange'].get('s', 1)
    self.param['d'] = step['gforinrange'].get('d', 0)
    self.param['i'] = step['gforinrange'].get('i', '')

    self.begin = self.counter
    self.end = self.begin + self.param['d']
    
    return


  def gforinrange_forward(self):
    # for i in range(x, y, s):
    if (self.counter > self.end) and (self.param['x'] < self.param['y']):
      self.param['x'] += self.param['s']
      # Update the step parameters
      # {"exec": "bsc.rotate", "useorig": true, "gforinrange": {"i": "angle", "x": 0, "y": 60, "s": 15, "d": 0}},
      i_name = self.step['gforinrange']['i']
      self.step[i_name] = self.param['x']
      return True

    return False


  def gforinrange_backward(self):
    # for i in range(x, y, s):
    if (self.counter > self.begin) and (self.param['x'] > 0):
      self.param['x'] = self.param['x'] - self.param['s']
      return True

    return False



  def next_counter(self):
    self.counter += 1
    if self.type == 'gforinrange':
      if self.gforinrange_forward():
        self.counter = self.begin

    return self.counter


  def prev_counter(self):
    self.counter -= 1
    if self.type == 'gforinrange':
      if self.gforinrange_backward():
        self.counter = self.end

    return self.counter
