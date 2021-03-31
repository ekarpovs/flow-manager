
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
    self.parent['bg'] = 'bisque'

    self.parent.update()
    h = self.parent.winfo_reqheight()
    w = self.parent.winfo_width()

    self.grid()
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)

    self.modules_frame = LabelFrame(self, bg="yellow", text='Modules', height=200, width=w)
    # self.modules_frame.grid_propagate(0)

    self.actions_frame = FlowActions(self)   

    self.modules_frame.grid(row=0, column=0, padx=PADX, pady=PADY)
    self.actions_frame.grid(row=4, column=0, padx=PADX, pady=PADY)


  def show_modules(self, modules):

    return


  def show_flows(self, flows):

    return


  def show_flow():

    return


  def show_image():

    return