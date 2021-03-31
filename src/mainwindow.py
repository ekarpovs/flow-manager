from tkinter import *

from .uiconst import *
from .mainactions import MainActions
from .flow import FlowController

class MainWindow():
  def __init__(self, root):
    self.root = root
    # self.PADX = 10
    # self.PADY = 10
   
    self.root.update()
    h = self.root.winfo_reqheight()
    w = self.root.winfo_width()

    self.main_frame = Frame(self.root)
    self.main_frame.grid()

    # create all of the main containers
    self.actions_frame = MainActions(self.main_frame)

    # flow_height = calculate_reminder_height(self.root, [self.actions_frame])

    self.flow_frame = Frame(self.main_frame)
    self.flow_controller = FlowController(self.flow_frame)

    # layout all of the main container
    # self.main_frame.rowconfigure(0, weight=1)
    # self.main_frame.columnconfigure(0, weight=1)

    self.flow_frame.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=E+W)
    self.actions_frame.grid(row=1, column=0, padx=PADX, pady=PADY, sticky=E+W)

    # do not resize the flow frame after a widget will be added
    flow_height = calculate_reminder_height(self.root, [self.actions_frame])
    self.flow_frame['height'] = flow_height
    self.flow_frame['width'] = w
    self.flow_frame.grid_propagate(0)

    # Bind to actions panel
    self.actions_frame.btn_exit.bind("<Button>", self.exit)

  def exit(self, event):
    exit(0)


