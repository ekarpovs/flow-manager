from .statement import Statement

class State:
  def __init__(self):
    self.reset()


  def reset(self):
    self.counter = -1
    self.steps = None
    self.statement = Statement(self)

    return    

  def ready(self):
    return self.counter > -1


  def set(self, steps):
    self.steps = steps
    self.counter = 0

    return

  def has_statement(self, step):
    statements = ['gforinrange', 'gif', 'gelese']
    
    # res = [ele for ele in listA if(ele in data_string)]
    # res = any(item in data_string for item in listA)

    has = any(item in step for item in statements)
    print("has")
    
    return has


  def next(self):
    step = None
    if self.counter < len(self.steps):
      step = self.steps[self.counter]
      self.statement.set(step)      
      self.counter = self.statement.next_counter()

    return self.counter, step


  def prev(self):
    step = None
    if self.counter > 0:
      self.counter = self.statement.prev_counter()
      step = self.steps[self.counter]

    return self.counter, step

  