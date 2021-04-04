from tkinter import *
from tkinter import ttk

from .flowmodel import FlowModel  
from .flowview import FlowView  

class FlowController():
  def __init__(self, parent):
    self.parent = parent

    print("CONTROLLER")

    self.model = FlowModel()
    self.view = FlowView(self.parent)

    self.work_sheet_names = []

    self.start()

# Common methods
  @classmethod
  def get_config():
    paths = []

    return paths

  def start(self):
    # bunding actions?
    # self.actions.btn_run.bind("<Button>", self.run)

    self.get_all()
    self.show_all()

    return


# Meta data
  def get_all(self):
    self.get_modules_meta()   
    self.get_work_sheet_names()
    self.get_work_sheet()

    return

  def get_modules_meta(self):
    self.modules_meta = self.model.get_modules_meta()

    return

  def get_work_sheet_names(self):
    self.work_sheet_names = self.model.get_work_sheet_names()


  def get_work_sheet(self, work_sheet_name="compare"):
    self.work_sheet = self.model.get_work_sheet(work_sheet_name)
  

  def show_all(self):
    self.show_modules_meta()
    self.show_work_sheet_names()
    self.show_work_sheet()

    return


  def show_modules_meta(self):
    self.view.show_modules_meta(self.modules_meta)

    return

  def show_work_sheet_names(self):
    self.view.show_work_sheet_names(self.work_sheet_names)


  def show_work_sheet(self):
    self.view.show_work_sheet(self.work_sheet)

    return
