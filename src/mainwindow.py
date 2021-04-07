from tkinter import *

from .uiconst import *
from .mainactions import MainActions
from .manager import MngrController

class MainWindow():
  def __init__(self, root):
    self.root = root
   
    self.main_frame = Frame(self.root, bg='bisque')
    self.main_frame.grid()

    # create all of the main containers
    self.actions_frame = MainActions(self.main_frame)

    self.flow_frame = Frame(self.main_frame)
    self.fit_flow_frame_size()
    self.flow_controller = MngrController(self.flow_frame)

    self.flow_frame.grid(row=0, column=0, sticky=E+W)
    self.actions_frame.grid(row=1, column=0, sticky=E+W)

    # Bind to actions panel
    self.actions_frame.btn_exit.bind("<Button>", self.exit)


  def fit_flow_frame_size(self):
    self.root.update()
    h = self.root.winfo_reqheight()
    w = self.root.winfo_width()
    flow_height = calculate_reminder_height(self.root, [self.actions_frame])
    self.flow_frame['height'] = flow_height
    self.flow_frame['width'] = w
    
    # do not resize the flow frame after a widget will be added
    self.flow_frame.grid_propagate(0)

  def exit(self, event):
    exit(0)


