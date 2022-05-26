from tkinter import *

from .uiconst import *
from .mainactions import MainActions
from .manager import MngrController

class MainWindow():
  def __init__(self, root):
    self.root = root
   
    self.main_frame = Frame(self.root, bg='bisque', name='mainframe')
    self.main_frame.grid()

    # create all of the main containers
    self.actions_frame = MainActions(self.main_frame)

    self.manager_frame = Frame(self.main_frame, name='managerframe')
    self.fit_manager_frame_size()
    self.flow_controller = MngrController(self.manager_frame)

    self.manager_frame.grid(row=0, column=0, sticky=E+W)
    self.actions_frame.grid(row=1, column=0, sticky=E+W)

    # Bind to actions panel
    self.actions_frame.btn_exit.bind("<Button>", self.exit)


  def fit_manager_frame_size(self):
    self.root.update()
    h = self.root.winfo_reqheight()
    w = self.root.winfo_width()
    flow_height = calculate_reminder_height(self.root, [self.actions_frame])
    self.manager_frame['height'] = flow_height
    self.manager_frame['width'] = w
    
    # do not resize the flow frame after a widget will be added
    self.manager_frame.grid_propagate(False)

  def exit(self, event):
    exit(0)


