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


    self._module = ModuleView(self)
    self._flow = FlowView(self)
    self._data = DataView(self)

    self._divide_view()

    self._module.grid(row=0, column=0)
    self._flow.grid(row=0, column=1)
    self._data.grid(row=0, column=2)


  @property
  def module(self) -> ModuleView:
    return self._module

  @property
  def flow(self) -> FlowView:
    return self._flow

  @property
  def data(self) -> DataView:
    return self._data


  @property
  def ws_names(self):
    return self._flow.ws_names

  @ws_names.setter
  def ws_names(self, ws_names):
    self._flow.ws_names = ws_names
    return

  def set(self, flow_module_name):
    self._flow.set_flow_module_name(flow_module_name)
    return

  @property
  def module_defs(self):
    return self._module.module_defs

  @module_defs.setter
  def module_defs(self, modules_defs):
    self._module.module_defs = modules_defs
    return


# View layout
################### Local methods ###########################
  def _divide_view(self):
    self.parent.update()
    h = self.parent.winfo_reqheight()
    w = self.parent.winfo_reqwidth()
    self['width'] = w -5
    self._module['height'] = h - PADY*2
    self._module['width'] = int((w/4)*0.9)
    self._flow['height'] = h - PADY*2
    self._flow['width'] = int((w/4)*1.02)
    self._data['height'] = h - PADY*2
    self._data['width'] = w - self._module['width'] - self._flow['width']
    self._module.grid_propagate(0)
    self._flow.grid_propagate(0)
    self._data.grid_propagate(0)
