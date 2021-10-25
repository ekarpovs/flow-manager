
from tkinter import *
from tkinter import ttk

from ..uiconst import *
from .views import *

class MngrView(LabelFrame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent

    self.grid()
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)
    self.columnconfigure(2, weight=2)


    self.modules_view = ModulesView(self)
    self.flows_view = FlowsView(self)
    self.images_view = ImagesView(self)

    self.divide_view()

    self.modules_view.grid(row=0, column=0)
    self.flows_view.grid(row=0, column=1)
    self.images_view.grid(row=0, column=2)


# Show Meta data
  def set_modules_meta(self, modules_meta):
    self.modules_view.set_modules_meta(modules_meta)

  @property
  def flows_names(self):
    return self.flows_view.flows_names

  @flows_names.setter
  def flows_names(self, flows_names):
    self.flows_view.flows_names = flows_names
    return

  def set(self, flow_module_name):
    self.flows_view.set_flow_module_name(flow_module_name)
    return

  @property
  def modules_defs(self):
    return self.modules_view.modules_defs

  @modules_defs.setter
  def modules_defs(self, modules_defs):
    self.modules_view.modules_defs = modules_defs
    return


# View state


################### Local methods ###########################
  def divide_view(self):
    self.parent.update()
    h = self.parent.winfo_reqheight()
    w = self.parent.winfo_reqwidth()
    self['width'] = w -5
    self.modules_view['height'] = h - PADY*2
    self.modules_view['width'] = int((w/4)*0.9)
    self.flows_view['height'] = h - PADY*2
    self.flows_view['width'] = int((w/4)*1.02)
    self.images_view['height'] = h - PADY*2
    self.images_view['width'] = w - self.modules_view['width'] - self.flows_view['width']
    self.modules_view.grid_propagate(0)
    self.flows_view.grid_propagate(0)
    self.images_view.grid_propagate(0)
