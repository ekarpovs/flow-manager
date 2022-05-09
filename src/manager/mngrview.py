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
    self.rowconfigure(1, weight=1)
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)
    self.columnconfigure(2, weight=1)
    self.columnconfigure(3, weight=2)


    self._module = ModuleView(self)
    self._flow = FlowView(self)
    self._links = LinksView(self)
    self._params = ParamsView(self)
    self._data = DataView(self)

    self._module.grid(row=0, column=0, rowspan=2, sticky=N+S)
    self._flow.grid(row=0, column=1, sticky=N+S)
    self._links.grid(row=1, column=1, sticky=N+S)
    self._params.grid(row=0, column=2, rowspan=2, sticky=N+S)
    self._data.grid(row=0, column=3, rowspan=2, sticky=N+S)
    self._divide_view()
    return

  @property
  def module(self) -> ModuleView:
    return self._module

  @property
  def flow(self) -> FlowView:
    return self._flow

  @property
  def params(self) -> ParamsView:
    return self._params

  @property
  def links(self) -> LinksView:
    return self._links

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

  @property
  def ws_title(self):
    return self._flow.ws_title

  @ws_title.setter
  def ws_title(self, ws_title):
    self._flow.ws_title = ws_title
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
    # self.parent.update()
    self.update_idletasks()
    h = self.parent.winfo_reqheight()
    w = self.parent.winfo_reqwidth()
    self['width'] = w - PADX_S
    view_height = h - PADY*2
    self._module['height'] = view_height
    self._module['width'] = w//5
    self._flow['height'] = int(view_height * 0.7)
    self._flow['width'] = int((w/4)*0.95)
    self._links['height'] = int(view_height * 0.3)
    self._links['width'] = int((w/4)*0.95)
    self._params['height'] = view_height
    self._params['width'] = int((w/5) * 1.1)
    self._data['height'] = view_height
    self._data['width'] = w - self._module['width'] - self._params['width'] - self._flow['width']-PADX
    self._module.grid_propagate(0)
    self._flow.grid_propagate(0)
    self._links.grid_propagate(0)
    self._params.grid_propagate(0)
    self._data.grid_propagate(0)
    return
