class State:
  def __init__(self):
    self.reset()


  def reset(self):
    self.counter = -1
    self.steps = None

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
      self.counter += 1

    return step


  def prev(self):
    step = None
    if self.counter > 0:
      self.counter -= 1
      step = self.steps[self.counter]

    return step

  