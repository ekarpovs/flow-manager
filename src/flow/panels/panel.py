from tkinter import *

from ...uiconst import *

class Panel(LabelFrame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 

    self['bd'] = 2
    self['relief'] = RIDGE