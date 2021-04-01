
from tkinter import *
from tkinter import ttk

from ..uiconst import *
from .panels import *
from .flowactions import FlowActions

class FlowView(LabelFrame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent

    self['bd'] = 2
    self['relief'] = RIDGE 
    self['bg'] = 'pink'

    self.grid()
    self.rowconfigure(0, weight=1)
    self.rowconfigure(1, weight=1)
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)
    self.columnconfigure(2, weight=2)


    self.actions_frame = FlowActions(self)   

    self.modules_frame = ModulesPanel(self)

    self.flows_frame = FlowsPanel(self)

    self.images_frame = ImagesPanel(self)

    self.divide_view()

    self.modules_frame.grid(row=0, column=0)
    self.flows_frame.grid(row=0, column=1)
    self.images_frame.grid(row=0, column=2)
    self.actions_frame.grid(row=1, column=0, sticky=W+S)

    self.show_flow([])

  def divide_view(self):
    self.parent.update()
    h = self.parent.winfo_reqheight()
    w = self.parent.winfo_reqwidth()
    self.actions_frame.update()
    ha = self.actions_frame.winfo_reqheight()
    self['width'] = w -5
    self.modules_frame['height'] = h - ha - PADY*2
    self.modules_frame['width'] = int(w/4)
    self.flows_frame['height'] = h - ha - PADY*2
    self.flows_frame['width'] = int(w/4)
    self.images_frame['height'] = h - ha - PADY*2
    self.images_frame['width'] = w - int(w/4)*2 - 5
    self.actions_frame['width'] = w
    # do not resize the flow frame after a widget will be added
    self.modules_frame.grid_propagate(0)
    self.flows_frame.grid_propagate(0)
    self.images_frame.grid_propagate(0)


  def show_modules(self, modules):

    return


  def show_flows(self, flows):

    return


  def show_flow(self, flow):
    self.flows_frame.set_flow(flow)

    return


  def show_image():

    return