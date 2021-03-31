from tkinter import *
from tkinter import ttk

from .flowmodel import FlowModel  
from .flowview import FlowView  

class FlowController():
  def __init__(self, parent):
    self.parent = parent

    self.model = FlowModel()
    self.view = FlowView(self.parent)

    self.start()


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

  
  def get_all(self):
    self.get_modules()
    self.get_flows()

    return


  def get_modules(self):
    ''' 
      Get modules & operations
    '''
    self.modules = []

    return


  def get_flows(self):
    ''' 
      Get modules & operations
    '''
    self.flows = []

    return

  def show_all(self):
    self.show_flows()
    self.show_modules()

    return


  def show_modules(self):
    # self.view.show_modules(self.modules)

    return


  def show_flows(self):
    # self.view.show_flows(self.flows)

    return


  def run():

    return