class Context:
  def __init__(self, **kwargs):
    self.kwargs_before = kwargs
    self.kwargs_after = None

  def set_after(self, **kwargs):
    self.kwargs_after = kwargs
