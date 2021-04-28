class Context:
  def __init__(self, idx, step_meta, **kwargs):
    self.idx = idx
    self.step_meta = step_meta
    self.kwargs_before = kwargs
    self.kwargs_after = None

  def set_after(self, **kwargs):
    self.kwargs_after = kwargs
