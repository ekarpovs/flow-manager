
from tkinter import *
from tkinter import ttk

from ..uiconst import *
from .views import *

class MngrView(LabelFrame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent

    self.grid()
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)
    self.columnconfigure(2, weight=2)


    self.modules_view = ModulesView(self)

    self.flows_view = FlowsView(self)

    self.output_view = ImagesView(self)

    self.divide_view()

    self.modules_view.grid(row=0, column=0)
    self.flows_view.grid(row=0, column=1)
    self.output_view.grid(row=0, column=2)


# Show Meta data
  def show_modules_meta(self, modules_meta):
    self.modules_view.set_modules_meta(modules_meta)


  def show_work_sheet_names(self, work_sheet_names):
    self.flows_view.set_work_sheet_names(work_sheet_names)

    return

  def show_work_sheet(self, work_sheet):
    self.flows_view.set_work_sheet(work_sheet)

    return



################### Local methods ###########################
  def divide_view(self):
    self.parent.update()
    h = self.parent.winfo_reqheight()
    w = self.parent.winfo_reqwidth()
    self['width'] = w -5
    self.modules_view['height'] = h - PADY*2
    self.modules_view['width'] = int(w/4)
    self.flows_view['height'] = h - PADY*2
    self.flows_view['width'] = int(w/4)
    self.output_view['height'] = h - PADY*2
    self.output_view['width'] = w - int(w/4)*2 - 5
    self.modules_view.grid_propagate(0)
    self.flows_view.grid_propagate(0)
    self.output_view.grid_propagate(0)
