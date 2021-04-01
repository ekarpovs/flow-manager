from tkinter import *
from tkinter import ttk

from .flowmodel import FlowModel  
from .flowview import FlowView  

class FlowController():
  def __init__(self, parent):
    self.parent = parent

    self.model = FlowModel()
    self.view = FlowView(self.parent)

    self.flow_names = []

    self.start()


  def get_flow_names(self):
    self.flow_names = self.model.get_flow_names()

  def show_flow_names(self):
    self.view.show_flow_names(self.flow_names)


  def get_flow_content(self, flow_name="compare"):
    self.flow = self.model.get_flow(flow_name)
  
  def show_flow_content(self):
    self.view.show_flow(self.flow)


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
    
    self.get_flow_names()
    
    self.get_flow_content()

    return


  def get_modules(self):
    ''' 
      Get modules & operations
    '''
    self.modules = []

    return


  def show_all(self):
    self.show_modules()
    self.show_flow_names()
    self.show_flow_content()

    return


  def show_modules(self):
    # self.view.show_modules(self.modules)

    return


  def show_flows(self):
    # self.view.show_flows(self.flows)

    return


  def run():

    return