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


    self.module_view = ModuleView(self)
    self.flow_view = FlowView(self)
    self.image_view = ImageView(self)

    self._divide_view()

    self.module_view.grid(row=0, column=0)
    self.flow_view.grid(row=0, column=1)
    self.image_view.grid(row=0, column=2)


  @property
  def flow_names(self):
    return self.flow_view.flow_names

  @flow_names.setter
  def flow_names(self, flows_names):
    self.flow_view.flow_names = flows_names
    return

  def set(self, flow_module_name):
    self.flow_view.set_flow_module_name(flow_module_name)
    return

  @property
  def module_defs(self):
    return self.module_view.module_defs

  @module_defs.setter
  def module_defs(self, modules_defs):
    self.module_view.module_defs = modules_defs
    return


# View state


################### Local methods ###########################
  def _divide_view(self):
    self.parent.update()
    h = self.parent.winfo_reqheight()
    w = self.parent.winfo_reqwidth()
    self['width'] = w -5
    self.module_view['height'] = h - PADY*2
    self.module_view['width'] = int((w/4)*0.9)
    self.flow_view['height'] = h - PADY*2
    self.flow_view['width'] = int((w/4)*1.02)
    self.image_view['height'] = h - PADY*2
    self.image_view['width'] = w - self.module_view['width'] - self.flow_view['width']
    self.module_view.grid_propagate(0)
    self.flow_view.grid_propagate(0)
    self.image_view.grid_propagate(0)
