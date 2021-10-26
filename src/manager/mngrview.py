from tkinter import *
from tkinter import ttk

from ..uiconst import *
from .views import *

class MngrView(LabelFrame):
  '''
  Fasade for views 
  '''
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent

    self.grid()
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)
    self.columnconfigure(2, weight=2)


    self.module = ModuleView(self)
    self.flow = FlowView(self)
    self.image = ImageView(self)

    self._divide_view()

    self.module.grid(row=0, column=0)
    self.flow.grid(row=0, column=1)
    self.image.grid(row=0, column=2)


  @property
  def flow_names(self):
    return self.flow.flow_names

  @flow_names.setter
  def flow_names(self, flows_names):
    self.flow.flow_names = flows_names
    return

  def set(self, flow_module_name):
    self.flow.set_flow_module_name(flow_module_name)
    return

  @property
  def module_defs(self):
    return self.module.module_defs

  @module_defs.setter
  def module_defs(self, modules_defs):
    self.module.module_defs = modules_defs
    return


# View state


################### Local methods ###########################
  def _divide_view(self):
    self.parent.update()
    h = self.parent.winfo_reqheight()
    w = self.parent.winfo_reqwidth()
    self['width'] = w -5
    self.module['height'] = h - PADY*2
    self.module['width'] = int((w/4)*0.9)
    self.flow['height'] = h - PADY*2
    self.flow['width'] = int((w/4)*1.02)
    self.image['height'] = h - PADY*2
    self.image['width'] = w - self.module['width'] - self.flow['width']
    self.module.grid_propagate(0)
    self.flow.grid_propagate(0)
    self.image.grid_propagate(0)
