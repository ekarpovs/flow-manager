from tkinter import *

from ...uiconst import *

class View(LabelFrame):
  def __init__(self, parent):
    super().__init__(parent)
    self._parent = parent 

    self._parent.update_idletasks()
    self._manager_container_h = self._parent.winfo_height()
    self._manager_container_w = self._parent.winfo_width()

    self['bd'] = 2
    self['relief'] = RIDGE