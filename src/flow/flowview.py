
from tkinter import *
from tkinter import ttk

from ..uiconst import *
from .flowactions import FlowActions

class FlowView(LabelFrame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent

    self['bd'] = 2
    self['relief'] = RIDGE 
    self['bg'] = 'pink'

    # self.parent.update()
    # h = self.parent.winfo_reqheight()
    # w = self.parent.winfo_reqwidth()

    self.grid()
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)


    self.actions_frame = FlowActions(self)   

    # self.modules_frame = LabelFrame(self, bg="yellow", text='Modules', height=h-200, width=w)
    self.modules_frame = LabelFrame(self, bg="yellow", text='Modules')
    self.fit_frames_size()

    self.modules_frame.grid(row=0, column=0)
    self.actions_frame.grid(row=4, column=0, sticky=W+S)


  def fit_frames_size(self):
    self.parent.update()
    h = self.parent.winfo_reqheight()
    w = self.parent.winfo_reqwidth()
    self.actions_frame.update()
    ha = self.actions_frame.winfo_reqheight()
    self.modules_frame['height'] = h - ha - PADY*2
    self.modules_frame['width'] = w - 5
    self.actions_frame['width'] = w
    # do not resize the flow frame after a widget will be added
    self.modules_frame.grid_propagate(0)


  def show_modules(self, modules):

    return


  def show_flows(self, flows):

    return


  def show_flow():

    return


  def show_image():

    return