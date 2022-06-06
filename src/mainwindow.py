from tkinter import *

from .uiconst import *
from .mainactions import MainActions
from .manager import MngrController

class MainWindow():
  def __init__(self, root):
    self._root = root

    # setup application geometry
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    root.geometry("{}x{}+{}+{}".format(sw, sh-SCREEN_FREE_AREA, 0,0))
    root.resizable(0, 0) 

    h = root.winfo_height()
    self._root.rowconfigure(0, weight=1)
    self._root.columnconfigure(0, weight=1)

    # setup main container
    self.main_container = Frame(self._root, height=h, name='mainframe')
    self.main_container.grid(row=0, column=0, sticky=N+S+E+W)
    self.main_container.rowconfigure(0, weight=1)
    self.main_container.columnconfigure(0, weight=1)

    # setup mainactions container
    self.actions_container = MainActions(self.main_container)

    # setup all manager's views container
    self.manager_container = Frame(self.main_container, name='managerframe', bg='bisque')
    self.fit_manager_container_size()

    self.manager_container.grid(row=0, column=0, sticky=E+W)
    self.actions_container.grid(row=1, column=0, sticky=E+W)

    # create main controller
    self.flow_controller = MngrController(self.manager_container)

    # Bind to actions panel
    self.actions_container.btn_exit.bind("<Button>", self.exit)


  def fit_manager_container_size(self):
    self._root.update()
    h = self._root.winfo_reqheight()
    w = self._root.winfo_width()
    flow_height = calculate_reminder_height(self._root, [self.actions_container])
    self.manager_container['height'] = flow_height
    self.manager_container['width'] = w
    
    # do not resize the flow frame after a widget will be added
    self.manager_container.grid_propagate(False)

  def exit(self, event):
    exit(0)


